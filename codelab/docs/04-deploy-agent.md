# 04 - Déployer l'agent

## Ce que vous allez faire

Déployer l'agent ADK sur Cloud Run et récupérer son URL officielle pour les étapes suivantes.

## Pourquoi c'est important

Le pont WhatsApp (étapes 05-06) dépend de l'URL de cet agent. Si ce déploiement est mal configuré, la chaîne complète échoue.

## Résultat attendu en fin d'étape

- Service Cloud Run `matos-agent-service` déployé
- variable `MATOS_AGENT_URL` définie
- interface ADK accessible

## 1. Préparer le contexte

```bash
cd agent
source venv/bin/activate
export BACKEND_URL="$MATOS_BACKEND_URL"
echo "BACKEND_URL=$BACKEND_URL"
```

Vérifiez aussi la présence de `.dockerignore` pour éviter l'upload du venv:

```bash
ls -la .dockerignore
```

## 2. Déployer le service agent

```bash
adk deploy cloud_run \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --service_name matos-agent-service \
  --with_ui
```

Important:

- gardez le nom `matos-agent-service`
- ne laissez pas le nom par défaut si vous voulez un workshop cohérent

## 3. Récupérer l'URL et sauvegarder la variable

```bash
export MATOS_AGENT_URL="$(gcloud run services describe matos-agent-service --region "$REGION" --format='value(status.url)')"
echo "$MATOS_AGENT_URL"
```

Optionnel (persistance shell):

```bash
echo "export MATOS_AGENT_URL=\"$MATOS_AGENT_URL\"" >> ~/.bashrc
source ~/.bashrc
```

## 4. Vérifier que le service est bien en ligne

```bash
gcloud run services describe matos-agent-service --region "$REGION" --format='value(status.url,status.traffic[0].percent)'
curl -I "$MATOS_AGENT_URL/dev-ui/"
```

Résultat attendu:

- le service existe
- `/dev-ui/` répond (200 ou redirection)

## 5. Checkpoint fonctionnel

Utilisez ensuite l'étape 07 pour valider le comportement end-to-end via le bridge WhatsApp.

## Troubleshooting rapide

### 1) `adk: command not found`

```bash
cd agent
source venv/bin/activate
pip install google-adk
adk --version
```

### 2) Service introuvable

```bash
gcloud run services list --project "$PROJECT_ID" --region "$REGION"
```

Si le nom n'est pas `matos-agent-service`, redéployez avec `--service_name matos-agent-service`.

### 3) L'agent ne trouve pas les produits

```bash
echo "$BACKEND_URL"
curl -fsS "$MATOS_BACKEND_URL/health"
```

Si nécessaire, réexportez `BACKEND_URL` puis redéployez.

Passez à `05 - Construire le pont WhatsApp`.