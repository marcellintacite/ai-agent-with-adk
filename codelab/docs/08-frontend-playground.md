# 08 - Frontend Playground (No Twilio)

Use this page if you want to test agent behavior from a browser without waiting for Twilio setup.

## Prerequisites

- `MATOS_AGENT_URL` is available (Step 04),
- `BRIDGE_URL` is available (Step 06, recommended),
- services are online.

## 1. Run frontend locally

```bash
cd frontend
python3 -m http.server 5174
```

Open:

```text
http://localhost:5174
```

## 2. Configure chat UI

1. Paste `BRIDGE_URL` in the URL field.
2. Keep or edit `userId`.
3. Send a test message.

Using `BRIDGE_URL` is recommended because it avoids CORS issues and matches the production request path.

## 3. Recommended test prompts

1. `Hello, I need a laptop`
2. `niko na tafuta machine ya 16go RAM`
3. `I want this model, my name is Amina, email amina@example.com`

## 4. Optional: deploy frontend on Cloud Run

```bash
cd frontend
gcloud builds submit --tag "gcr.io/$PROJECT_ID/matos-frontend:v1" .
gcloud run deploy matos-frontend \
  --image "gcr.io/$PROJECT_ID/matos-frontend:v1" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --port 8080
export FRONTEND_URL="$(gcloud run services describe matos-frontend --region "$REGION" --format='value(status.url)')"
echo "$FRONTEND_URL"
```

## 5. If messages fail

```bash
gcloud run services logs read matos-whatsapp-bridge --region "$REGION" --limit 50
gcloud run services logs read matos-agent-service --region "$REGION" --limit 50
```

Check that the frontend is calling `POST /chat` on the bridge URL.