# 06 - Déployer le pont WhatsApp

Déployez le bridge sur Cloud Run. Vous pouvez continuer avec ou sans compte Twilio.

## 1. Construire l'image du bridge

```bash
cd backend
gcloud builds submit --tag "gcr.io/$PROJECT_ID/matos-whatsapp-bridge:v1" .
```

## 2A. Déployer sans Twilio (parcours de test web)

```bash
gcloud run deploy matos-whatsapp-bridge \
  --image "gcr.io/$PROJECT_ID/matos-whatsapp-bridge:v1" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars "ADK_SERVICE_URL=$MATOS_AGENT_URL,ADK_APP_NAME=matos"
```

## 2B. Déployer avec Twilio (parcours WhatsApp complet)

Créer ou mettre à jour les secrets une fois :

```bash
echo "$TWILIO_ACCOUNT_SID" | gcloud secrets create twilio_account_sid --data-file=- 2>/dev/null || echo "$TWILIO_ACCOUNT_SID" | gcloud secrets versions add twilio_account_sid --data-file=-
echo "$TWILIO_AUTH_TOKEN" | gcloud secrets create twilio_auth_token --data-file=- 2>/dev/null || echo "$TWILIO_AUTH_TOKEN" | gcloud secrets versions add twilio_auth_token --data-file=-
```

Déployer avec les paramètres Twilio :

```bash
gcloud run deploy matos-whatsapp-bridge \
  --image "gcr.io/$PROJECT_ID/matos-whatsapp-bridge:v1" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars "ADK_SERVICE_URL=$MATOS_AGENT_URL,ADK_APP_NAME=matos,TWILIO_FROM_NUMBER=whatsapp:+14155238886,OWNER_PHONE=whatsapp:+243999537410" \
  --set-secrets "TWILIO_ACCOUNT_SID=twilio_account_sid:latest,TWILIO_AUTH_TOKEN=twilio_auth_token:latest"
```

## 3. Enregistrer et vérifier l'URL du bridge

```bash
export BRIDGE_URL="$(gcloud run services describe matos-whatsapp-bridge --region "$REGION" --format='value(status.url)')"
echo "$BRIDGE_URL"
curl -fsS "$BRIDGE_URL/health"
```

## 4. Vérification fonctionnelle

- Parcours Twilio : définissez `WHEN A MESSAGE COMES IN` sur `${BRIDGE_URL}/webhook/twilio` dans Twilio Sandbox.
- Parcours sans Twilio :

```bash
curl -fsS -X POST "$BRIDGE_URL/chat" -H "Content-Type: application/json" -d '{"message":"Hello, I am looking for a laptop"}'
```

## Vérification

Continuez lorsque `BRIDGE_URL` est définie et que `/health` répond.

Suite : `07 - Validation and Troubleshooting`