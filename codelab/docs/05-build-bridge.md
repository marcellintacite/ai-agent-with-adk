# 05 - Construire le pont WhatsApp

Cette étape explique le role du service `backend/` avant le déploiement.

## Pourquoi ce service existe

Le bridge connecte les webhooks Twilio au runtime de l'agent. Il permet de séparer les préoccupations du canal de la logique IA.

Résumé du flux :

1. Recevoir le webhook WhatsApp.
2. Valider la signature Twilio.
3. Appeler le service agent.
4. Retourner la réponse de l'agent.

La logique métier reste dans :

- `matos-agent-service` pour le raisonnement et l'utilisation des outils,
- `matos-backend` pour les données produit/client.

## Variables d'environnement requises

- `ADK_SERVICE_URL` : URL de l'agent déployé,
- `ADK_APP_NAME` : nom de l'application déployée (`matos`),
- `TWILIO_ACCOUNT_SID` : ID de compte Twilio (optionnel si vous n'utilisez pas encore le parcours WhatsApp),
- `TWILIO_AUTH_TOKEN` : secret webhook Twilio (optionnel pour un parcours non-Twilio),
- `TWILIO_FROM_NUMBER` : numero d'envoi WhatsApp,
- `OWNER_PHONE` : numero de notification proprietaire.

## Endpoints du bridge

- `POST /webhook/twilio`
- `POST /chat`
- `GET /health`

## Vérification

Vous etes pret pour le déploiement lorsque vous comprenez les responsabilités du bridge et les variables requises.

Suite : `06 - Deploy the WhatsApp Bridge`
