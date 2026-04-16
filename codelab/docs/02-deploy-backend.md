# 02 - Déployer le backend Matos

Dans cette étape, vous déployez le backend Matos en premier, puis vous sauvegardez son URL.

## Pourquoi ce backend est important

Ce backend est la source de vérité de votre agent:

- il contient le catalogue produits,
- il enregistre les prospects (clients),
- il fournit des endpoints que l'agent va appeler pour répondre correctement.

Sans ce backend, l'agent ne peut pas lire de vraies données.

## Résultat attendu

À la fin de cette étape:

- le service `matos-backend-service` est déployé sur Cloud Run,
- la variable `MATOS_BACKEND_URL` est définie,
- l'endpoint `/health` répond `status: ok`.

## 1. Construire l'image du backend

Exécutez:

```bash
gcloud builds submit --tag "gcr.io/$PROJECT_ID/matos-backend:v1" ./matos-backend
```

## 2. Déployer le service sur Cloud Run

Exécutez:

```bash
gcloud run deploy matos-backend-service \
  --image "gcr.io/$PROJECT_ID/matos-backend:v1" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --port 8080
```

## 3. Récupérer l'URL du service

Exécutez:

```bash
export MATOS_BACKEND_URL="$(gcloud run services describe matos-backend-service --region "$REGION" --format='value(status.url)')"
```

Exécutez:

```bash
echo "$MATOS_BACKEND_URL"
```

## 4. Tester la santé du service

Exécutez:

```bash
curl -fsS "$MATOS_BACKEND_URL/health"
```

Vous devez voir un JSON avec `"status":"ok"`.

## 5. Endpoints disponibles

Le backend expose ces endpoints:

- `GET /health`  
  Vérifie que le service est en ligne.

- `GET /products`  
  Liste les produits.

- `GET /products/{product_id}`  
  Détail d'un produit.

- `GET /products/categories`  
  Liste des catégories disponibles.

- `GET /customers`  
  Liste des clients/prospects enregistrés.

- `GET /customers/{customer_id}`  
  Détail d'un client.

- `POST /customers`  
  Crée un nouveau prospect.

- `PUT /customers/{customer_id}`  
  Met à jour un prospect existant.

- `DELETE /customers/{customer_id}`  
  Supprime un prospect.

## 6. Tests rapides des endpoints principaux

Test produits:

```bash
curl -fsS "$MATOS_BACKEND_URL/products" | head
```

Test catégories:

```bash
curl -fsS "$MATOS_BACKEND_URL/products/categories"
```

Test recherche texte:

```bash
curl -fsS "$MATOS_BACKEND_URL/products?q=laptop"
```

Test filtre catégorie:

```bash
curl -fsS "$MATOS_BACKEND_URL/products?category=laptops"
```

Test création prospect:

```bash
curl -fsS -X POST "$MATOS_BACKEND_URL/customers" -H "Content-Type: application/json" -d '{"full_name":"Amina Bahati","email":"amina@example.com"}'
```

## 7. Vérifier le déploiement

Assurez-vous que l'URL est sauvegardée et que le service répond.

Passez à `03 - Construire l'agent`.