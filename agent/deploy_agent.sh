#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-}"
REGION="${REGION:-}"
BACKEND_URL="${BACKEND_URL:-}"
SERVICE_NAME="${SERVICE_NAME:-matos-agent-service}"

if [[ -z "$PROJECT_ID" || -z "$REGION" || -z "$BACKEND_URL" ]]; then
  echo "Usage: set PROJECT_ID, REGION, and BACKEND_URL before running this script."
  echo "Example:"
  echo "  export PROJECT_ID=your-project-id"
  echo "  export REGION=europe-west1"
  echo "  export BACKEND_URL=https://matos-backend-service-xxxx.run.app"
  echo "  ./deploy_agent.sh"
  exit 1
fi

echo "[1/4] Deploying ADK agent service (${SERVICE_NAME})"
cd "$(dirname "$0")/matos"
adk deploy cloud_run \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --service_name "$SERVICE_NAME" \
  --with_ui \
  .

echo "[2/4] Setting BACKEND_URL on Cloud Run service"
gcloud run services update "$SERVICE_NAME" \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --set-env-vars "BACKEND_URL=${BACKEND_URL}"

echo "[3/4] Reading deployed URL"
MATOS_AGENT_URL="$(gcloud run services describe "$SERVICE_NAME" --project "$PROJECT_ID" --region "$REGION" --format='value(status.url)')"

echo "[4/4] Verifying env var on service"
gcloud run services describe "$SERVICE_NAME" \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --format='flattened(spec.template.spec.containers[0].env[])' | grep BACKEND_URL || true

echo "Agent deployed successfully"
echo "MATOS_AGENT_URL=${MATOS_AGENT_URL}"
echo "Run this in your shell:"
echo "export MATOS_AGENT_URL=\"${MATOS_AGENT_URL}\""
