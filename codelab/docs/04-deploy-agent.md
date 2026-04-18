# 04 - Déployer l'agent

Cette étape déploie le service agent sur Cloud Run.

## Résultat attendu

- `matos-agent-service` est déployé,
- `MATOS_AGENT_URL` est exportée,
- l'interface dev UI est accessible.

## 1. Déployer depuis le bon dossier

```bash
cd agent/matos
source ../venv/bin/activate
export BACKEND_URL="$MATOS_BACKEND_URL"
adk deploy cloud_run --project "$PROJECT_ID" --region "$REGION" --service_name matos-agent-service --with_ui .
```

## 2. Enregistrer l'URL du service

```bash
export MATOS_AGENT_URL="$(gcloud run services describe matos-agent-service --region "$REGION" --format='value(status.url)')"
echo "$MATOS_AGENT_URL"
```

## 3. Valider le déploiement

```bash
curl -I "$MATOS_AGENT_URL/dev-ui/"
curl -I "$MATOS_AGENT_URL/dev/build_graph_image/matos?dark_mode=true"
```

Si les deux endpoints répondent, continuez.

Suite : `05 - Build the WhatsApp Bridge`
