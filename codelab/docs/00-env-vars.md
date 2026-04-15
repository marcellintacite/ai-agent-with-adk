# 00 - Variables d'environnement (Cloud Shell)

Utilisez cette page comme source unique de vérité pour les variables de l'atelier.

## 1. Variables de base requises

```bash
export PROJECT_ID="votre-id-projet-gcp"
export REGION="africa-south1"
```

Si un service n'est pas disponible dans cette region, basculez vers:

```bash
export REGION="us-central1"
```

## 2. Variables d'URL de service (Définir après déploiement)

```bash
# Après déploiement de matos-backend
export MATOS_BACKEND_URL="https://..."

# Après déploiement de l'agent
export MATOS_AGENT_URL="https://..."

# Après déploiement du pont
export BRIDGE_URL="https://..."
```

## 3. Variables Twilio optionnelles (Cloud Shell)

Utilisez des secrets en production. Pour les démos d'atelier, vous pouvez exporter temporairement :

```bash
export TWILIO_ACCOUNT_SID="ACxxxxxxxx"
export TWILIO_AUTH_TOKEN="xxxxxxxx"
```

## 4. Vérification rapide

```bash
echo "$PROJECT_ID"
echo "$REGION"
echo "$MATOS_BACKEND_URL"
echo "$MATOS_AGENT_URL"
echo "$BRIDGE_URL"
```

Si une variable s'affiche vide, redéfinissez-la avant de passer à l'étape suivante.
