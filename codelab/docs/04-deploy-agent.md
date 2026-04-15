# 04 - Déployer l'agent

Après avoir construit l'agent, nous le déployons et sauvegardons son URL.

## 1. Déployer le service agent

Depuis `agent/`, déployez le service ADK.

```bash
cd agent

# Important: l'agent doit connaitre votre backend deploye
export BACKEND_URL="$MATOS_BACKEND_URL"

adk deploy cloud_run \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --service_name matos-agent-service \
  --with_ui

export MATOS_AGENT_URL="$(gcloud run services describe matos-agent-service --region "$REGION" --format='value(status.url)')"
echo "$MATOS_AGENT_URL"
```

Si vos fonctions d'outils appellent l'URL backend, assurez-vous que `BACKEND_URL=$MATOS_BACKEND_URL` est configuré pour l'agent déployé.

Passez à `05 - Construire le pont WhatsApp`.