import httpx
from contextlib import asynccontextmanager
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

from src.config import settings
from src.logger import setup_logging, logger

# --- Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(settings.LOG_LEVEL)
    app.state.http = httpx.AsyncClient(timeout=30.0)
    logger.info("Bridge started", 
                adk_url=settings.ADK_SERVICE_URL, 
                app_name=settings.ADK_APP_NAME)

    yield
    await app.state.http.aclose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Webhook bridge to the ADK Agent service.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Helpers ---


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


# --- Routes ---


class WebChatRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    message: str
    user_id: Optional[str] = Field(default=None, alias="userId")


class WebChatResponse(BaseModel):
    reply: str
    user_id: str

@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.APP_NAME, "version": settings.VERSION}


@app.post("/chat", response_model=WebChatResponse)
async def web_chat(data: WebChatRequest):
    """CORS-friendly endpoint to test the agent from a web frontend."""
    message = data.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="message is required")

    user_id = (data.user_id or "").strip() or f"web-{uuid4().hex[:8]}"
    logger.info("Received web chat message", user=user_id)

    reply = await call_adk_agent(app.state.http, user_id, message)
    return WebChatResponse(reply=reply, user_id=user_id)
