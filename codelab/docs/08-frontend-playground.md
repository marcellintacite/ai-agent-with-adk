# 08 - Frontend Playground (webhook/chat)

Cette étape est le chemin principal pour tester l'agent depuis un navigateur.

## Prérequis

- `MATOS_AGENT_URL` est disponible (Étape 04),
- `BRIDGE_URL` est disponible (recommandé),
- les services sont en ligne.

Si vous n'avez pas encore `BRIDGE_URL`, déployez le bridge rapidement :

```bash
cd backend
chmod +x deploy_bridge.sh
./deploy_bridge.sh
```

Le script lit `PROJECT_ID`, `REGION` et `MATOS_AGENT_URL`, puis construit et déploie automatiquement le service `matos-bridge`.

## 1. Lancer le frontend localement

```bash
cd frontend
python3 -m http.server 5174
```

Ouvrez :

```text
http://localhost:5174
```

## 2. Configurer l'interface

1. Collez `BRIDGE_URL` dans le champ URL.
2. Gardez ou modifiez `userId`.
3. Envoyez un message de test.

L'utilisation de `BRIDGE_URL` est recommandée car elle évite les problèmes CORS et reproduit le chemin de requête de production.

## 3. Prompts recommandés

1. `Hello, I need a laptop`
2. `niko na tafuta machine ya 16go RAM`
3. `I want this model, my name is Amina, email amina@example.com`

## 4. Optionnel : déployer le frontend sur Cloud Run

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

## 5. En cas d'échec des messages

```bash
gcloud run services logs read matos-bridge --region "$REGION" --limit 50
gcloud run services logs read matos-agent-service --region "$REGION" --limit 50
```

Vérifiez que le frontend appelle bien `POST /chat` sur l'URL du bridge.

Après cette étape, vous pouvez ajouter un webhook vers WhatsApp, Telegram ou une autre plateforme en réutilisant le même bridge.