# 02 - Déployer le backend Matos

Dans cette étape, nous déployons le backend Matos en premier et sauvegardons son URL pour les étapes suivantes.

## 1. Déployer le backend

```bash
gcloud builds submit --tag "gcr.io/$PROJECT_ID/matos-backend:v1" ./matos-backend

gcloud run deploy matos-backend-service \
  --image "gcr.io/$PROJECT_ID/matos-backend:v1" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --port 8080

export MATOS_BACKEND_URL="$(gcloud run services describe matos-backend-service --region "$REGION" --format='value(status.url)')"
echo "$MATOS_BACKEND_URL"
curl -fsS "$MATOS_BACKEND_URL/health"
```

## 2. Vérifier le déploiement

Assurez-vous que l'URL est sauvegardée et que le service répond.

Passez à `03 - Construire l'agent`.