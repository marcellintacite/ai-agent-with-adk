# 05 - Construire le pont WhatsApp

## Objectif de cette page

Dans cette étape, vous préparez le service `backend/` qui fait le lien entre WhatsApp (Twilio) et votre agent.

Ce service s'appelle "bridge" (pont), car il transporte les messages entre le canal et l'agent.

## Pourquoi ce bridge est nécessaire

L'agent sait réfléchir et appeler vos outils métier.

Mais WhatsApp n'appelle pas directement l'agent avec le bon format. Il faut une couche intermédiaire qui:

1. reçoit les messages entrants,
2. valide la sécurité de la requête,
3. appelle l'agent,
4. renvoie la réponse vers WhatsApp.

Sans ce bridge, Twilio et l'agent ne peuvent pas communiquer correctement.

## Pourquoi Twilio dans cet atelier

Twilio est utilisé ici comme **exemple de canal**.

L'idée importante est la suivante:

- votre agent est le cerveau
- Twilio est seulement un transport

Vous pouvez brancher le même agent sur d'autres canaux plus tard:

- web chat
- application mobile
- Telegram, Messenger, Slack
- call center tooling

## Ce que le bridge fait (et ne fait pas)

Le bridge fait:

- transport des messages,
- validation de signature,
- appel de l'agent,
- retour de réponse vers le canal.

Le bridge ne fait pas:

- la logique métier produit,
- la recommandation intelligente,
- la gestion du catalogue.

Ces responsabilités restent dans:

- `matos-agent-service` (intelligence),
- `matos-backend` (données).

## Architecture simple

Le service `backend/` (bridge) reste volontairement mince:

1. recevoir un message entrant depuis un canal
2. valider la requête du canal (ex: signature Twilio)
3. appeler l'agent (`/run`)
4. renvoyer la réponse au canal

## Flux d'un message (pas à pas)

1. Le client écrit sur WhatsApp.
2. Twilio envoie un webhook au bridge (`POST /webhook/twilio`).
3. Le bridge vérifie la signature Twilio.
4. Le bridge appelle l'agent.
5. L'agent interroge le backend si nécessaire.
6. L'agent renvoie une réponse.
7. Le bridge renvoie cette réponse à Twilio.
8. Le client reçoit le message sur WhatsApp.

## Variables d'environnement requises

Au déploiement du bridge, vous injectez:

- `ADK_SERVICE_URL`  
	URL publique du service agent.

- `ADK_APP_NAME`  
	Nom de l'app agent appelée par le bridge.

- `TWILIO_ACCOUNT_SID`  
	Identifiant du compte Twilio.

- `TWILIO_AUTH_TOKEN`  
	Secret Twilio pour valider les webhooks entrants.

- `TWILIO_FROM_NUMBER`  
	Numéro WhatsApp utilisé pour envoyer les réponses.

- `OWNER_PHONE`  
	Numéro du propriétaire pour les notifications.

## Endpoints du bridge

- `POST /webhook/twilio`: reçoit les messages WhatsApp entrants
- `POST /notify/owner`: envoie une notification au propriétaire
- `GET /health`: vérifie que le service est en ligne

## Résultat attendu en fin d'étape

À ce stade, vous devez comprendre clairement:

- pourquoi ce service existe,
- quelles variables il consomme,
- quels endpoints seront testés après déploiement.

## Important: Twilio est un exemple, pas une limite

Si vous ne souhaitez pas finaliser Twilio maintenant, vous pourrez tester l'agent avec une interface web locale en fin de workshop.

Continuez d'abord avec le parcours principal Twilio.

Passez à `06 - Déployer le pont WhatsApp`.
