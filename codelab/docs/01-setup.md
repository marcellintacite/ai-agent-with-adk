# 01 - Configuration (Cloud Shell en premier)

Cet atelier est conçu pour Google Cloud Shell + éditeur intégré.

Objectif de cette étape: préparer un environnement propre, puis deployer service par service (pas tout en une fois).

## 1. Réclamer les crédits Cloud

Allez sur [Google Cloud Free Tier](https://cloud.google.com/free) et réclamez vos crédits gratuits si vous ne l'avez pas encore fait.

## 2. Créer un projet GCP

1. Allez sur [Google Cloud Console](https://console.cloud.google.com/).
2. Créez un nouveau projet ou sélectionnez un projet existant.
3. Notez l'ID du projet (par exemple, `my-matos-project`).

## 2.1 Choisir une region (recommandation Bukavu)

Bukavu n'a pas de region GCP locale. Une option souvent choisie en pratique est:

- `africa-south1` (Johannesburg) si disponible sur les services utilises.

Si un service n'est pas disponible dans cette region, utilisez temporairement `us-central1` pour le workshop.

## 3. Ouvrir Cloud Shell

1. Dans la console GCP, cliquez sur l'icône Cloud Shell en haut à droite.
2. Attendez que le shell se charge.

## 4. Cloner le dépôt dans Cloud Shell

```bash
git clone <VOTRE_URL_REPO>
cd build_with_ai_workshop
```

## 5. Ouvrir l'éditeur

Dans Cloud Shell, cliquez sur "Ouvrir l'éditeur" pour lancer l'éditeur intégré.

## 6. Ajouter les variables de base dans le shell

```bash
export PROJECT_ID="votre-id-projet-gcp"
export REGION="africa-south1"

gcloud config set project "$PROJECT_ID"
gcloud auth login
gcloud auth application-default login
```

## 7. Activer les APIs requises

```bash
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    aiplatform.googleapis.com
```

## 8. Préparer le sandbox Twilio

1. Créez/compte sur Twilio.
2. Ouvrez le sandbox WhatsApp.
3. Rejoignez le sandbox depuis votre WhatsApp en utilisant le code de jonction fourni.

## 9. Installer les outils d'exécution dans Cloud Shell

```bash
python3 --version
node --version
npm --version

pip install --user -r agents/requirements.txt
pip install --user -r backend/requirements.txt
pip install --user -r matos-backend/requirements.txt
```

Si votre dossier s'appelle `agent/` (singulier), utilisez:

```bash
pip install --user -r agent/requirements.txt
```

## 10. Confirmer la disposition des dossiers

```text
build_with_ai_workshop/
├── matos-backend/         # API produit et client
├── agent/                 # Code agent (root_agent.py)
├── backend/               # Pont WhatsApp Twilio
└── codelab/               # Docs atelier
```

Passez à `02 - Déployer le backend`.
