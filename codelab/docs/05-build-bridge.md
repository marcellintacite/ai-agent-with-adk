# 05 - Construire le pont WhatsApp

## Ce que vous allez faire

Dans cette étape, vous préparez une couche d'integration entre un canal de messagerie (Twilio WhatsApp) et votre agent ADK.

## Pourquoi Twilio ici

Twilio est utilise dans ce workshop comme **exemple de canal**.

L'idee importante est la suivante:

- votre agent est le cerveau
- Twilio est seulement un transport

Vous pouvez brancher le meme agent sur d'autres canaux plus tard:

- web chat
- application mobile
- Telegram, Messenger, Slack
- call center tooling

## Architecture simple

Le service `backend/` (bridge) reste volontairement mince:

1. recevoir un message entrant depuis un canal
2. valider la requete du canal (ex: signature Twilio)
3. appeler l'agent (`/run`)
4. renvoyer la reponse au canal

Le bridge ne porte pas la logique metier produit. Cette logique reste dans:

- l'agent ADK
- `matos-backend`

## Variables d'environnement requises

Au deploiement du bridge, vous injectez:

- `ADK_SERVICE_URL`
- `ADK_APP_NAME`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM_NUMBER`
- `OWNER_PHONE`

## Endpoints du bridge

- `POST /webhook/twilio`: webhook entrant WhatsApp
- `POST /notify/owner`: notification proprietaire
- `GET /health`: verification service

## Important: Twilio est un exemple, pas une limite

Si vous ne souhaitez pas finaliser Twilio maintenant, vous pourrez tester l'agent avec une interface web locale en fin de workshop.

Continuez d'abord avec le parcours principal Twilio.

Passez a `06 - Deployer le pont WhatsApp`.
