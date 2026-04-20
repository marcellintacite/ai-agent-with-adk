# 04 - Déployer l'agent

Cette étape déploie le service agent sur Cloud Run.

## Résultat attendu

- `matos-agent-service` est déployé,
- `MATOS_AGENT_URL` est exportée,
- `BACKEND_URL` est bien présent dans la configuration Cloud Run,
- l'interface dev UI est accessible.

## 1. Déployer depuis le bon dossier

```bash
cd agent
source venv/bin/activate
export BACKEND_URL="$MATOS_BACKEND_URL"
chmod +x deploy_agent.sh
./deploy_agent.sh
```

## 2. Enregistrer l'URL du service

```bash
export MATOS_AGENT_URL="$(gcloud run services describe matos-agent-service --region "$REGION" --format='value(status.url)')"
echo "$MATOS_AGENT_URL"
```

## 3. Vérifier que BACKEND_URL est bien attaché au service

```bash
gcloud run services describe matos-agent-service \
	--region "$REGION" \
	--format='flattened(spec.template.spec.containers[0].env[])' | grep BACKEND_URL
```

## 4. Valider le déploiement

```bash
curl -I "$MATOS_AGENT_URL/dev-ui/"
curl -I "$MATOS_AGENT_URL/dev/build_graph_image/matos?dark_mode=true"
```

Si les deux endpoints répondent, continuez.

Suite : `08 - Frontend Playground (webhook/chat)`
