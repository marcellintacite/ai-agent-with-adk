# 06 - Déployer le pont WhatsApp

Dans cette étape, vous déployez le service bridge sur Cloud Run.

Important: il y a 2 parcours possibles:

- Parcours A: vous n'avez pas de compte Twilio (vous continuez quand même)
- Parcours B: vous avez un compte Twilio (intégration WhatsApp complète)

## 1. Construire l'image du bridge

Exécutez:

```bash
cd backend
```

```bash
gcloud builds submit --tag "gcr.io/$PROJECT_ID/matos-whatsapp-bridge:v1" .
```

## 2A. Déployer le bridge (sans compte Twilio)

Si vous n'avez pas de compte Twilio, utilisez cette commande (sans `--set-secrets`):

```bash
gcloud run deploy matos-whatsapp-bridge \
  --image "gcr.io/$PROJECT_ID/matos-whatsapp-bridge:v1" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars "ADK_SERVICE_URL=$MATOS_AGENT_URL,ADK_APP_NAME=matos"
```

Ce mode vous permet de continuer l'atelier et de tester via le frontend (`/chat`) même sans WhatsApp.

## 2B. Déployer le bridge (avec compte Twilio)

Utilisez cette commande si vous avez déjà les secrets `twilio_account_sid` et `twilio_auth_token` dans Secret Manager:

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

### Version simplifiée (si vous avez déjà les valeurs)

Si vous avez déjà `TWILIO_ACCOUNT_SID` et `TWILIO_AUTH_TOKEN`, faites juste ça:

```bash
echo "$TWILIO_ACCOUNT_SID" | gcloud secrets create twilio_account_sid --data-file=- 2>/dev/null || echo "$TWILIO_ACCOUNT_SID" | gcloud secrets versions add twilio_account_sid --data-file=-
```

```bash
echo "$TWILIO_AUTH_TOKEN" | gcloud secrets create twilio_auth_token --data-file=- 2>/dev/null || echo "$TWILIO_AUTH_TOKEN" | gcloud secrets versions add twilio_auth_token --data-file=-
```

```bash
gcloud run deploy matos-whatsapp-bridge --image "gcr.io/$PROJECT_ID/matos-whatsapp-bridge:v1" --region "$REGION" --platform managed --allow-unauthenticated --port 8080 --set-env-vars "ADK_SERVICE_URL=$MATOS_AGENT_URL,ADK_APP_NAME=matos,TWILIO_FROM_NUMBER=whatsapp:+14155238886,OWNER_PHONE=whatsapp:+243999537410" --set-secrets "TWILIO_ACCOUNT_SID=twilio_account_sid:latest,TWILIO_AUTH_TOKEN=twilio_auth_token:latest"
```

```bash
export BRIDGE_URL="$(gcloud run services describe matos-whatsapp-bridge --region "$REGION" --format='value(status.url)')" && echo "$BRIDGE_URL"
```

### Si vous n'avez pas encore créé les secrets Twilio

La commande `--set-secrets` lit les secrets depuis **Secret Manager** (pas directement depuis vos variables d'environnement shell).

Vous avez 2 façons de créer ces secrets:

#### Option 1: vous avez déjà les valeurs dans des variables d'environnement

Exécutez:

```bash
echo "$TWILIO_ACCOUNT_SID" | gcloud secrets create twilio_account_sid --data-file=-
```

```bash
echo "$TWILIO_AUTH_TOKEN" | gcloud secrets create twilio_auth_token --data-file=-
```

Si le secret existe déjà, mettez à jour la version:

```bash
echo "$TWILIO_ACCOUNT_SID" | gcloud secrets versions add twilio_account_sid --data-file=-
```

```bash
echo "$TWILIO_AUTH_TOKEN" | gcloud secrets versions add twilio_auth_token --data-file=-
```

#### Option 2: vous n'avez pas de variables d'environnement, vous tapez les valeurs

Exécutez:

```bash
read -s TWILIO_ACCOUNT_SID && echo
```

```bash
echo "$TWILIO_ACCOUNT_SID" | gcloud secrets create twilio_account_sid --data-file=-
```

```bash
read -s TWILIO_AUTH_TOKEN && echo
```

```bash
echo "$TWILIO_AUTH_TOKEN" | gcloud secrets create twilio_auth_token --data-file=-
```

Vérifiez que les 2 secrets existent:

```bash
gcloud secrets list | grep -E "twilio_account_sid|twilio_auth_token"
```

## 3. Récupérer l'URL du bridge et tester la santé

Exécutez:

```bash
export BRIDGE_URL="$(gcloud run services describe matos-whatsapp-bridge --region "$REGION" --format='value(status.url)')"
```

```bash
echo "$BRIDGE_URL"
```

```bash
curl -fsS "$BRIDGE_URL/health"
```

## 4. Configuration Twilio (uniquement parcours B)

Si vous avez Twilio, dans Twilio Sandbox, définissez `WHEN A MESSAGE COMES IN` à:

```text
${BRIDGE_URL}/webhook/twilio
```

## 5. Si vous n'avez pas Twilio: test alternatif immédiat

Vous pouvez tester le bridge sans Twilio avec l'endpoint web:

```bash
curl -fsS -X POST "$BRIDGE_URL/chat" -H "Content-Type: application/json" -d '{"message":"Bonjour, je cherche un laptop"}'
```

Si une réponse JSON revient, votre bridge est opérationnel.

## 6. Résumé des variables finales

Exécutez:

```bash
echo "MATOS_BACKEND_URL=$MATOS_BACKEND_URL"
```

```bash
echo "MATOS_AGENT_URL=$MATOS_AGENT_URL"
```

```bash
echo "BRIDGE_URL=$BRIDGE_URL"
```

## 7. Checkpoint de sortie

Vous pouvez passer à l'étape 07 si:

- `BRIDGE_URL` est non vide,
- `/health` répond,
- et selon votre parcours:
  - parcours A (sans Twilio): `/chat` répond correctement,
  - parcours B (avec Twilio): webhook sandbox configuré.

Passez à `07 - Validation et dépannage`.