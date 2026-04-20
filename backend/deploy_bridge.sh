#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-}"
REGION="${REGION:-}"
MATOS_AGENT_URL="${MATOS_AGENT_URL:-}"

SERVICE_NAME="${SERVICE_NAME:-matos-bridge}"
IMAGE_TAG="${IMAGE_TAG:-v1}"
ADK_APP_NAME="${ADK_APP_NAME:-matos}"

if [[ -z "$PROJECT_ID" || -z "$REGION" || -z "$MATOS_AGENT_URL" ]]; then
  echo "Usage: set PROJECT_ID, REGION, and MATOS_AGENT_URL before running this script."
  echo "Example:"
  echo "  export PROJECT_ID=your-project-id"
  echo "  export REGION=us-central1"
  echo "  export MATOS_AGENT_URL=https://matos-agent-service-xxxx.run.app"
  echo "  ./deploy_bridge.sh"
  exit 1
fi

IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:${IMAGE_TAG}"

echo "[1/3] Building bridge image: ${IMAGE}"
gcloud builds submit --project "$PROJECT_ID" --tag "$IMAGE" .

echo "[2/3] Deploying Cloud Run service: ${SERVICE_NAME}"
gcloud run deploy "$SERVICE_NAME" \
  --project "$PROJECT_ID" \
  --image "$IMAGE" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars "ADK_SERVICE_URL=${MATOS_AGENT_URL},ADK_APP_NAME=${ADK_APP_NAME}"

BRIDGE_URL="$(gcloud run services describe "$SERVICE_NAME" --project "$PROJECT_ID" --region "$REGION" --format='value(status.url)')"

echo "[3/3] Bridge deployed successfully"
echo "BRIDGE_URL=${BRIDGE_URL}"
echo "Run this in your shell:"
echo "export BRIDGE_URL=\"${BRIDGE_URL}\""
