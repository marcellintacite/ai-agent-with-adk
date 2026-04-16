# 04 - Déployer l'agent

## Objectif de cette page

Dans cette étape, vous faites une seule chose: déployer l'agent sur Cloud Run.

À la fin, vous aurez:

- un service Cloud Run `matos-agent-service` en ligne,
- une URL d'agent sauvegardée dans `MATOS_AGENT_URL`,
- une interface de test accessible.

## 1. Préparer le contexte de déploiement

Avant de lancer le déploiement, vérifiez uniquement ces points:

- `PROJECT_ID` est défini,
- `REGION` est défini (atelier: `europe-west1`),
- `MATOS_BACKEND_URL` est défini,
- vous êtes dans le dossier `agent/`,
- l'environnement virtuel est activé.

Exécutez:

```bash
cd agent
```

```bash
source venv/bin/activate
```

```bash
export BACKEND_URL="$MATOS_BACKEND_URL"
```

Vérifiez:

```bash
echo "PROJECT_ID=$PROJECT_ID"
```

```bash
echo "REGION=$REGION"
```

```bash
echo "BACKEND_URL=$BACKEND_URL"
```

Si une valeur est vide, corrigez-la avant de continuer.

## 2. Déployer l'agent sur Cloud Run

Exécutez la commande de déploiement:

```bash
adk deploy cloud_run --project "$PROJECT_ID" --region "$REGION" --service_name matos-agent-service --with_ui .
```

Explication simple de cette commande:

- `adk deploy cloud_run`: demande à ADK de construire et déployer l'agent,
- `--project`: indique dans quel projet GCP déployer,
- `--region`: indique la région du service,
- `--service_name matos-agent-service`: fixe le nom du service,
- `--with_ui`: active l'interface web de test,
- `.`: utilise le dossier courant (`agent/`) comme source.

## 3. Récupérer l'URL du service déployé

Exécutez:

```bash
export MATOS_AGENT_URL="$(gcloud run services describe matos-agent-service --region "$REGION" --format='value(status.url)')"
```

Puis:

```bash
echo "$MATOS_AGENT_URL"
```

## 4. Vérifier que l'agent est bien en ligne

Exécutez:

```bash
gcloud run services describe matos-agent-service --region "$REGION" --format='value(status.url,status.traffic[0].percent)'
```

Puis testez l'interface:

```bash
curl -I "$MATOS_AGENT_URL/dev-ui/"
```

Résultat attendu:

- le service existe,
- le trafic est bien routé,
- `/dev-ui/` répond (200 ou redirection).

## 5. Checkpoint de sortie

Vous pouvez passer à l'étape suivante si:

- `MATOS_AGENT_URL` est non vide,
- `curl -I "$MATOS_AGENT_URL/dev-ui/"` répond,
- le nom du service est bien `matos-agent-service`.

Passez à `05 - Construire le pont WhatsApp`.
