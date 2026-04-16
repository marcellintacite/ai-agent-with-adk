# 01 - Configuration (Cloud Shell)

## Objectif de cette page

À la fin de cette étape, vous devez avoir:

- un projet Google Cloud sélectionné,
- le dépôt du workshop cloné,
- le dossier du projet ouvert dans l'éditeur Cloud Shell.

Cette étape est la base de tout le workshop. Si elle est propre, le reste devient simple.

## Ce que vous allez préparer

- Le contexte GCP (`PROJECT_ID`, `REGION`)
- Les APIs nécessaires au déploiement
- Les dépendances des services
- L'espace de travail visible dans l'éditeur

## 1. Ouvrir Google Cloud et vérifier votre projet

1. Ouvrez [Google Cloud Console](https://console.cloud.google.com/).
2. En haut de la page, vérifiez le projet actif.
3. Si nécessaire, créez un projet et notez son ID (exemple: `ladycraft1-4ee09`).

## 2. Ouvrir Cloud Shell

1. Cliquez sur l'icône Cloud Shell (terminal) dans la barre supérieure.
2. Attendez que le terminal soit prêt.
3. Vérifiez que `gcloud` répond:

```bash
gcloud --version
```

Résultat attendu: la version de `gcloud` s'affiche.

## 3. Initialiser les variables de base (ligne par ligne)

Exécutez:

```bash
export PROJECT_ID="votre-id-projet-gcp"
```

Testez:

```bash
echo "$PROJECT_ID"
```

Exécutez:

```bash
export REGION="europe-west1"
```

Testez:

```bash
echo "$REGION"
```

## 4. Lier Cloud Shell à votre projet GCP

Exécutez:

```bash
gcloud config set project "$PROJECT_ID"
```

Testez:

```bash
gcloud config get-value project
```

Le résultat doit être exactement votre `PROJECT_ID`.

## 5. Authentification (si demandée)

Exécutez uniquement si Cloud Shell vous le demande:

```bash
gcloud auth login
```

```bash
gcloud auth application-default login
```

## 6. Cloner le dépôt du workshop

Exécutez:

```bash
git clone https://github.com/marcellintacite/ai-agent-with-adk
```

Entrez dans le dossier:

```bash
cd build_with_ai_workshop
```

Testez que vous êtes au bon endroit:

```bash
pwd
```

Le chemin doit se terminer par `build_with_ai_workshop`.

## 7. Ouvrir le projet dans l'éditeur Cloud Shell (objectif principal)

Depuis le terminal Cloud Shell, exécutez:

```bash
cloudshell workspace .
```

Si la commande n'est pas disponible, ouvrez l'éditeur manuellement:

1. Cliquez sur **Open Editor** dans Cloud Shell.
2. Dans l'explorateur de fichiers, ouvrez le dossier `build_with_ai_workshop`.

Vérification visuelle attendue:

- vous voyez les dossiers `agent/`, `backend/`, `matos-backend/`, `codelab/`, `frontend/`.
- vous pouvez ouvrir `codelab/docs/intro.md` dans l'éditeur.

## 8. Activer les APIs requises

Exécutez:

```bash
gcloud services enable run.googleapis.com
```

```bash
gcloud services enable cloudbuild.googleapis.com
```

```bash
gcloud services enable artifactregistry.googleapis.com
```

```bash
gcloud services enable aiplatform.googleapis.com
```

```bash
gcloud services enable secretmanager.googleapis.com
```

Testez:

```bash
gcloud services list --enabled | grep -E "run.googleapis.com|cloudbuild.googleapis.com|artifactregistry.googleapis.com|aiplatform.googleapis.com|secretmanager.googleapis.com"
```

## 9. Vérifier les outils locaux

Exécutez:

```bash
python3 --version
```

```bash
node --version
```

```bash
npm --version
```

## 10. Installer les dépendances Python (ligne par ligne)

Exécutez:

```bash
pip install --user -r agent/requirements.txt
```

```bash
pip install --user -r backend/requirements.txt
```

```bash
pip install --user -r matos-backend/requirements.txt
```

Note: le dossier correct est `agent/` (singulier), pas `agents/`.

## 11. Checkpoint final

Avant de passer à l'étape 02, confirmez:

- `PROJECT_ID` et `REGION` sont définis.
- le projet GCP actif est correct.
- le dossier `build_with_ai_workshop` est ouvert dans l'éditeur Cloud Shell.
- les APIs sont activées.
- les dépendances Python sont installées.

Passez ensuite à `02 - Déployer le backend`.
