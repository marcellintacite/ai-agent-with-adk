import os
import httpx
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional
from uuid import uuid4

from fastapi import FastAPI, Form, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from twilio.request_validator import RequestValidator
from twilio.rest import Client

from src.config import settings
from src.logger import setup_logging, logger

# --- Auth ---
validator = RequestValidator(settings.TWILIO_AUTH_TOKEN) if settings.TWILIO_AUTH_TOKEN else None

# --- Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(settings.LOG_LEVEL)
    app.state.http = httpx.AsyncClient(timeout=30.0)
    logger.info("🚀 WhatsApp Bridge started", 
                adk_url=settings.ADK_SERVICE_URL, 
                app_name=settings.ADK_APP_NAME)
    
    if not validator:
        logger.warning("⚠️ TWILIO_AUTH_TOKEN not set — signature verification DISABLED!")
    
    yield
    await app.state.http.aclose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Twilio WhatsApp to ADK Agent bridge.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Helpers ---

async def verify_twilio_signature(request: Request):
    if not validator:
        return

    signature = request.headers.get("X-Twilio-Signature")
    if not signature:
        logger.warning("Request missing X-Twilio-Signature header")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing X-Twilio-Signature")

    url = str(request.url)
    if url.startswith("http://"):
        url = url.replace("http://", "https://", 1)

    form_data = await request.form()
    params = {k: v for k, v in form_data.items()}

    if not validator.validate(url, params, signature):
        logger.warning("Invalid Twilio signature", url=url)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid signature")


async def call_adk_agent(http: httpx.AsyncClient, user_id: str, message: str) -> str:
    payload = {
        "appName": settings.ADK_APP_NAME,
        "userId": user_id,
        "sessionId": user_id,
        "newMessage": {
            "role": "user",
            "parts": [{"text": message}],
        },
    }

    run_url = f"{settings.ADK_SERVICE_URL}/run"
    logger.info("Calling ADK agent", user=user_id, msg=message[:50])
    
    try:
        response = await http.post(run_url, json=payload)
        
        # Auto-create session if missing
        if response.status_code == 404:
            logger.info("Session not found, auto-creating...", user=user_id)
            create_url = f"{settings.ADK_SERVICE_URL}/apps/{settings.ADK_APP_NAME}/users/{user_id}/sessions/{user_id}"
            await http.post(create_url)
            response = await http.post(run_url, json=payload)

        response.raise_for_status()
        events = response.json()
        
        reply_parts = []
        for event in events:
            content = event.get("content") or {}
            if content.get("role") == "model":
                for part in content.get("parts", []):
                    if text := part.get("text", "").strip():
                        reply_parts.append(text)

        return reply_parts[-1] if reply_parts else "No response from sales assistant."
    except Exception as exc:
        logger.error("ADK Agent communication failed", error=str(exc))
        return "I'm having trouble connecting to my brain. Please try again later."


def make_twiml(message: str) -> str:
    from xml.sax.saxutils import escape
    safe = escape(message)
    return f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{safe}</Message></Response>'


# --- Routes ---

class LeadRequest(BaseModel):
    name: str
    contact_info: str


class WebChatRequest(BaseModel):
    message: str
    user_id: str | None = None


class WebChatResponse(BaseModel):
    reply: str
    user_id: str

@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.APP_NAME, "version": settings.VERSION}

@app.post("/webhook/twilio")
async def twilio_webhook(request: Request, From: str = Form(...), Body: str = Form(...)):
    # await verify_twilio_signature(request) # Optional: enable if Twilio Auth Token is live
    
    user_phone = From.replace("whatsapp:", "")
    logger.info("Received WhatsApp message", sender=user_phone)
    
    agent_reply = await call_adk_agent(app.state.http, user_phone, Body)
    
    return Response(
        content=make_twiml(agent_reply),
        media_type="application/xml"
    )

@app.post("/notify/owner")
async def notify_owner(data: LeadRequest):
    """Bridge for agent tools to notify the business owner."""
    logger.info("Dispatching lead notification to owner", customer=data.name)
    
    sid = settings.TWILIO_ACCOUNT_SID
    token = settings.TWILIO_AUTH_TOKEN
    
    if not (sid and token):
        logger.error("Twilio credentials missing for OWNER notification")
        raise HTTPException(status_code=500, detail="Bridge credentials missing")

    try:
        client = Client(sid, token)
        msg_body = (
            f"🛍️ *New Lead from Matos Bot*\n\n"
            f"*Name:* {data.name}\n"
            f"*Contact:* {data.contact_info}\n\n"
            f"Please follow up ASAP."
        )
        client.messages.create(
            to=settings.OWNER_PHONE,
            from_=settings.TWILIO_FROM_NUMBER,
            body=msg_body
        )
        return {"status": "notification_sent"}
    except Exception as exc:
        logger.error("Twilio notification failed", error=str(exc))
        raise HTTPException(status_code=500, detail="Notification failed")


@app.post("/chat", response_model=WebChatResponse)
async def web_chat(data: WebChatRequest):
    """CORS-friendly endpoint to test the agent from a web frontend without Twilio webhooks."""
    message = data.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="message is required")

    user_id = (data.user_id or "").strip() or f"web-{uuid4().hex[:8]}"
    logger.info("Received web chat message", user=user_id)

    reply = await call_adk_agent(app.state.http, user_id, message)
    return WebChatResponse(reply=reply, user_id=user_id)
