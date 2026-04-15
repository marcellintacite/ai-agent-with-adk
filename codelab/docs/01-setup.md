# 01 - Configuration (Cloud Shell)

## Ce que vous allez faire

Dans cette étape, vous préparez un environnement propre et reproductible pour tout le workshop.

## Pourquoi c'est important

Si la base n'est pas propre (projet, région, APIs, dépendances), les erreurs apparaissent plus tard pendant les déploiements et sont plus difficiles à diagnostiquer.

## Résultat attendu en fin d'étape

- Vous avez un projet GCP actif.
- Cloud Shell est prêt avec les APIs nécessaires.
- Les dépendances Python des 3 services sont installées.
- Le sandbox Twilio est prêt pour les tests WhatsApp.

## 1. Crédits et projet GCP

1. Activez vos crédits sur [Google Cloud Free Tier](https://cloud.google.com/free) si nécessaire.
2. Ouvrez [Google Cloud Console](https://console.cloud.google.com/).
3. Créez un projet ou réutilisez un projet existant.
4. Notez son ID (exemple: `my-matos-project`).

## 2. Choisir la région

Pour Bukavu, utilisez en priorité:

- `africa-south1` (Johannesburg)

Si un service n'est pas disponible, basculez sur:

- `us-central1`

## 3. Ouvrir Cloud Shell et cloner le dépôt

```bash
git clone https://github.com/marcellintacite/ai-agent-with-adk
cd build_with_ai_workshop
```

Ouvrez ensuite l'éditeur Cloud Shell pour travailler visuellement sur les fichiers.

## 4. Initialiser le contexte GCP

```bash
export PROJECT_ID="votre-id-projet-gcp"
export REGION="africa-south1"

gcloud config set project "$PROJECT_ID"
gcloud auth login
gcloud auth application-default login
```

### Vérification

```bash
gcloud config get-value project
echo "$REGION"
```

Vous devez voir votre `PROJECT_ID` et votre région.

## 5. Activer les APIs requises

```bash
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    aiplatform.googleapis.com
```

### Vérification

```bash
gcloud services list --enabled | grep -E "run.googleapis.com|cloudbuild.googleapis.com|artifactregistry.googleapis.com|aiplatform.googleapis.com"
```

## 6. Installer les dépendances des services

```bash
python3 --version
node --version
npm --version

pip install --user -r agent/requirements.txt
pip install --user -r backend/requirements.txt
pip install --user -r matos-backend/requirements.txt
```

Note: le dossier correct est `agent/` (singulier), pas `agents/`.

## 7. Préparer le sandbox Twilio

1. Connectez-vous à Twilio.
2. Ouvrez le WhatsApp Sandbox.
3. Rejoignez le sandbox depuis votre WhatsApp avec le code fourni par Twilio.

## 8. Checkpoint de sortie

Avant de passer à l'étape 02, confirmez:

- Le projet GCP est sélectionné.
- Les APIs sont activées.
- Les commandes `python3`, `node`, `npm` répondent.
- Les dépendances des 3 services sont installées sans erreur bloquante.
- Votre numéro de test a rejoint le sandbox Twilio.

Passez à `02 - Déployer le backend`.
