# 00 - Variables d'environnement

Cette page est votre référence rapide pour les variables utilisées pendant l'atelier.

## Variables principales

| Variable | Exemple | Définie à l'étape |
|----------|---------|-------------------|
| `PROJECT_ID` | `my-project-12345` | Étape 01 |
| `REGION` | `europe-west1` | Étape 01 |
| `MATOS_BACKEND_URL` | `https://matos-backend-service-...run.app` | Étape 02 |
| `MATOS_AGENT_URL` | `https://matos-agent-service-...run.app` | Étape 04 |
| `BRIDGE_URL` | `https://matos-bridge-...run.app` | Étape 08 |

## Configuration à faire une seule fois (par session de terminal)

Pour les variables d'environnement : ouvrez d'abord l'éditeur, puis ouvrez le terminal.

Exécutez ceci uniquement lorsque vous ouvrez une nouvelle session de terminal :

```bash
export PROJECT_ID="your-gcp-project-id"
export REGION="europe-west1"
```

Ensuite, définissez les URLs des services dans leurs étapes dédiées (02, 04, 08). Cela permet de garder chaque étape claire et d'éviter de redéclarer les variables inutilement.
