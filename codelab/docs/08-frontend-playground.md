# 08 - Frontend de test (sans Twilio)

## Ce que vous allez faire

Vous allez lancer un petit chat web local pour parler directement a l'agent ADK.

## Pourquoi cette option existe

Dans un workshop, tout le monde n'arrive pas au meme rythme sur Twilio (sandbox, webhook, secrets, numero de test).

Ce frontend sert de plan B pedagogique:

- vous validez l'intelligence de l'agent
- vous testez les prompts et les tools
- vous continuez l'atelier meme sans Twilio

## Prerequis

- `MATOS_AGENT_URL` est deja disponible (etape 04)
- `BRIDGE_URL` est idealement deja disponible (etape 06)
- l'agent repond en ligne

## 1. Lancer le frontend

Depuis la racine du projet:

```bash
cd frontend
python3 -m http.server 5174
```

Ouvrez ensuite:

```text
http://localhost:5174
```

## 2. Configurer le chat

Dans l'interface:

1. collez `BRIDGE_URL` (recommande)
2. gardez ou adaptez `userId`
3. envoyez un message test

Pourquoi `BRIDGE_URL` est recommande:

- evite les problemes CORS du navigateur
- reproduit mieux le flux production (canal -> bridge -> agent)

## 3. Scenarios recommandes

1. `Bonjour, je cherche un laptop`
2. `niko na tafuta machine ya 16go RAM`
3. `Je prends ce modele, je m'appelle Amina, email amina@example.com`

## 4. Déployer le frontend sur Cloud Run (optionnel)

Si vous voulez partager cette interface avec les participants, deployez-la comme un service web statique:

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

Resultat attendu:

- l'UI chat est accessible publiquement
- vous pouvez y coller `BRIDGE_URL` et tester l'agent

## 5. Si ca ne repond pas

- verifier que l'URL agent est correcte
- verifier que `BRIDGE_URL` est correcte
- verifier que le service `matos-whatsapp-bridge` est bien deploye
- verifier les logs Cloud Run du bridge puis de l'agent

```bash
gcloud run services logs read matos-whatsapp-bridge --region "$REGION" --limit 50
gcloud run services logs read matos-agent-service --region "$REGION" --limit 50
```

## Note technique

Le frontend appelle le bridge sur `POST /chat`, et le bridge appelle l'agent.
Cette architecture reduit fortement les problemes CORS et garde un chemin de test proche de la production.