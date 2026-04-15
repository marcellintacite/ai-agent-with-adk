# 06 - Déployer le pont WhatsApp

Après avoir construit le pont, nous le déployons et configurons Twilio.

## 1. Déployer le pont

```bash
cd backend

gcloud builds submit --tag "gcr.io/$PROJECT_ID/matos-whatsapp-bridge:v1" .

gcloud run deploy matos-whatsapp-bridge \
  --image "gcr.io/$PROJECT_ID/matos-whatsapp-bridge:v1" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars "ADK_SERVICE_URL=$MATOS_AGENT_URL,ADK_APP_NAME=matos_agent,TWILIO_FROM_NUMBER=whatsapp:+14155238886,OWNER_PHONE=whatsapp:+243999537410" \
  --set-secrets "TWILIO_ACCOUNT_SID=twilio_account_sid:latest,TWILIO_AUTH_TOKEN=twilio_auth_token:latest"

export BRIDGE_URL="$(gcloud run services describe matos-whatsapp-bridge --region "$REGION" --format='value(status.url)')"
echo "$BRIDGE_URL"
curl -fsS "$BRIDGE_URL/health"
```

## 2. Configurer le webhook Twilio Sandbox

Définissez `WHEN A MESSAGE COMES IN` à :

```text
${BRIDGE_URL}/webhook/twilio
```

## 3. Résumé des variables finales

```bash
echo "MATOS_BACKEND_URL=$MATOS_BACKEND_URL"
echo "MATOS_AGENT_URL=$MATOS_AGENT_URL"
echo "BRIDGE_URL=$BRIDGE_URL"
```

Passez à `07 - Validation et dépannage`.