# 05 - Construire le pont WhatsApp

Dans cette étape, nous connectons Twilio au service agent déployé.

## 1. Responsabilité du pont

`backend` est une couche de transport mince :

1. Recevoir les données de formulaire webhook Twilio.
2. Valider la signature Twilio.
3. Transférer le texte utilisateur vers ADK `/run`.
4. Retourner la réponse TwiML à Twilio.

Le pont ne contient pas de logique de catalogue métier. Celle-ci reste dans l'agent et l'API Matos.

## 2. Variables d'environnement requises

Définissez celles-ci au moment du déploiement :

- `ADK_SERVICE_URL`
- `ADK_APP_NAME`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM_NUMBER`
- `OWNER_PHONE`

## 3. Points de terminaison principaux

- `POST /webhook/twilio` -> reçoit le message entrant WhatsApp.
- `POST /notify/owner` -> point de terminaison de notification propriétaire optionnel.
- `GET /health` -> vérification de santé.

## 4. URL webhook Twilio

Après déploiement, configurez le webhook sandbox vers :

```text
https://<BRIDGE_URL>/webhook/twilio
```

Passez a `06 - Deployer le pont WhatsApp`.
