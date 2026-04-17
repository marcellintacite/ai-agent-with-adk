# 01 - Configuration et Démarrage Rapide

## Objectif
Préparez votre projet en 5 minutes: shell → éditeur → configuration → prêt.

## 1. Ouvrir la console Google Cloud

1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Vérifiez quel projet est actif en haut
3. Au besoin, créez un nouveau projet et notez son ID (ex: `my-project-12345`)

## 2. Ouvrir Cloud Shell

Cliquez sur l'icône Cloud Shell (>_) dans la barre d'outils en haut et attendez qu'elle soit prête.

## 3. Cloner le dépôt du workshop

```bash
git clone https://github.com/marcellintacite/ai-agent-with-adk
cd ai-agent-with-adk
```

## 4. Ouvrir l'éditeur

Depuis Cloud Shell, exécutez:

```bash
cloudshell editor
```

Ou cliquez sur le bouton **Open Editor**. Naviguez pour ouvrir le dossier `ai-agent-with-adk`.

Vous devriez voir: `agent/`, `backend/`, `matos-backend/`, `codelab/`, `frontend/`

## 5. Ouvrir un terminal dans l'éditeur

Cliquez sur **Terminal** → **New Terminal** dans le menu de l'éditeur (ou Ctrl+`)

## 6. Configurer votre projet et région

```bash
export PROJECT_ID="votre-id-projet-gcp"
export REGION="europe-west1"
```

Vérifiez:
```bash
gcloud config set project "$PROJECT_ID"
gcloud config get-value project
```

## 7. Enable All Required APIs (One Command)

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com aiplatform.googleapis.com secretmanager.googleapis.com
```

Verify with:
```bash
gcloud services list --enabled | grep googleapis
```

## 8. Install Python Dependencies

```bash
pip install --user -r agent/requirements.txt -r backend/requirements.txt -r matos-backend/requirements.txt
```

## Done ✓

You're ready. The variables `$PROJECT_ID` and `$REGION` are now set in your terminal session. 

Next: [Deploy Backend](02-deploy-backend.md)
- le projet GCP actif est correct.
- le dossier `build_with_ai_workshop` est ouvert dans l'éditeur Cloud Shell.
- les APIs sont activées.
- les dépendances Python sont installées.

Passez ensuite à `02 - Déployer le backend`.
