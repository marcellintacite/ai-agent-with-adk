# 01 - Setup (Quick Start)

## Goal
Get your project ready in 5 minutes: shell → editor → setup → done.

## 1. Open Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Check which project is active at the top
3. If needed, create a new project and note its ID (e.g., `my-project-12345`)

## 2. Open Cloud Shell

Click the Cloud Shell icon (>_) in the top toolbar and wait for it to be ready.

## 3. Clone the workshop repository

```bash
git clone https://github.com/marcellintacite/ai-agent-with-adk
cd build_with_ai_workshop
```

## 4. Open the Editor

From Cloud Shell, run:

```bash
cloudshell editor
```

Or click **Open Editor** button. Navigate to open the `build_with_ai_workshop` folder.

You should see: `agent/`, `backend/`, `matos-backend/`, `codelab/`, `frontend/`

## 5. Open Terminal in the Editor

Click **Terminal** → **New Terminal** in the editor menu (or Ctrl+`)

## 6. Set your Project & Region

```bash
export PROJECT_ID="your-gcp-project-id"
export REGION="europe-west1"
```

Verify:
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
