# 08 - Frontend Playground (webhook/chat)

Cette étape est le chemin principal pour tester l'agent depuis le frontend déployé.

## Prérequis

- `MATOS_AGENT_URL` est disponible (Étape 04),
- `BRIDGE_URL` est disponible,
- les services sont en ligne.

Si vous n'avez pas encore `BRIDGE_URL`, déployez le bridge rapidement :

```bash
cd backend
chmod +x deploy_bridge.sh
./deploy_bridge.sh
```

Le script lit `PROJECT_ID`, `REGION` et `MATOS_AGENT_URL`, puis construit et déploie automatiquement le service `matos-bridge`.

Vous pouvez retrouver l'URL du webhook ici :

```bash
echo "$BRIDGE_URL"
echo "${BRIDGE_URL}/chat"
```

Si `BRIDGE_URL` n'est pas exportee dans votre session :

```bash
export BRIDGE_URL="$(gcloud run services describe matos-bridge --region "$REGION" --format='value(status.url)')"
echo "$BRIDGE_URL"
```

Le webhook frontend a utiliser est : `${BRIDGE_URL}/chat`.

## 1. Déployer le frontend sur Cloud Run

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

## 2. Tester depuis le frontend déployé

1. Ouvrez `FRONTEND_URL` dans le navigateur.
2. Collez `BRIDGE_URL` dans le champ URL de l'interface.
3. Gardez ou modifiez `userId`, puis envoyez un message de test.

## 3. En cas d'échec des messages

```bash
gcloud run services logs read matos-bridge --region "$REGION" --limit 50
gcloud run services logs read matos-agent-service --region "$REGION" --limit 50
```

Vérifiez que le frontend appelle bien `POST /chat` sur l'URL du bridge.

Après cette étape, vous pouvez ajouter un webhook vers WhatsApp, Telegram ou une autre plateforme en réutilisant le même bridge.