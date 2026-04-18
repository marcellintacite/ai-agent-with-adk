# 01 - Configuration (Démarrage rapide)

## Objectif

Préparer votre espace de travail en environ 5 minutes.

## 1. Ouvrir Google Cloud Console

1. Allez sur [Google Cloud Console](https://console.cloud.google.com/).
2. Confirmez le projet actif.
3. Si nécessaire, créez un projet et notez son ID (par exemple `my-project-12345`).

## 2. Ouvrir Cloud Shell

Cliquez sur l'icône Cloud Shell (>_) dans la barre supérieure et attendez son initialisation.

## 3. Cloner le dépôt

```bash
git clone https://github.com/marcellintacite/ai-agent-with-adk
cd ai-agent-with-adk
```

## 4. Ouvrir Cloud Shell Editor

```bash
cloudshell editor
```

Ouvrez le dossier `ai-agent-with-adk`. Vous devriez voir `agent/`, `backend/`, `matos-backend/`, `codelab/` et `frontend/`.

## 5. Définir les variables du projet

```bash
export PROJECT_ID="your-gcp-project-id"
export REGION="europe-west1"
gcloud config set project "$PROJECT_ID"
```

## 6. Activer les APIs Google Cloud requises

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com aiplatform.googleapis.com secretmanager.googleapis.com
```

## 7. Installer les dépendances Python de l'atelier

```bash
pip install --user -r agent/requirements.txt -r backend/requirements.txt -r matos-backend/requirements.txt
```

## Vérification

Vous êtes prêt à continuer lorsque :

- `PROJECT_ID` est défini,
- les APIs requises sont activées,
- les dépendances sont installées.

Suite : [02 - Deploy Backend](02-deploy-backend.md)
