# 02 - Deployer le backend Matos

Dans cette étape, vous déployez d'abord le backend puis vous enregistrez son URL pour les étapes suivantes.

## Résultat attendu

- le service Cloud Run `matos-backend-service` est en ligne,
- `MATOS_BACKEND_URL` est exportée,
- la vérification de santé réussit.

## 1. Construire l'image du backend

```bash
gcloud builds submit --tag "gcr.io/$PROJECT_ID/matos-backend:v1" ./matos-backend
```

## 2. Déployer le backend sur Cloud Run

```bash
gcloud run deploy matos-backend-service \
  --image "gcr.io/$PROJECT_ID/matos-backend:v1" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --port 8080
```

## 3. Enregistrer l'URL du backend

```bash
export MATOS_BACKEND_URL="$(gcloud run services describe matos-backend-service --region "$REGION" --format='value(status.url)')"
echo "$MATOS_BACKEND_URL"
```

## 4. Valider le backend

```bash
curl -fsS "$MATOS_BACKEND_URL/health"
curl -fsS "$MATOS_BACKEND_URL/products?category=laptops" | head
```

Si les deux commandes retournent des données, passez à la suite.

Suite : `03 - Build the Agent`