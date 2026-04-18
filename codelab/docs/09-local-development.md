# 09 - Exécution locale complète

Cette page explique comment lancer toute la pile en local, sans Google Cloud.

## Résultat attendu

- `matos-backend` tourne en local,
- l'agent parle au backend local,
- le bridge expose `/chat` et `/health` en local,
- le frontend web permet de tester le flux complet.

## Prérequis pour l'agent

Avant de lancer l'agent, vérifiez que vos variables d'environnement sont bien définies.

Au minimum, configurez :

```bash
export BACKEND_URL="http://localhost:8081"
export GOOGLE_API_KEY="votre-cle-gemini"
```

Pour obtenir votre clé Gemini, connectez-vous sur [Google AI Studio](https://aistudio.google.com/) puis générez une nouvelle clé API.

Vous pouvez aussi placer ces valeurs dans `agent/.env` si vous préférez ne pas les exporter à chaque terminal.

## 0. Cloner le dépôt

Si vous partez de zéro en local, commencez par cloner le repo :

```bash
git clone https://github.com/marcellintacite/ai-agent-with-adk
cd ai-agent-with-adk
```

## 1. Démarrer le backend Matos

Dans un premier terminal :

```bash
cd /Users/aksantibahiga/Documents/build_with_ai_workshop/matos-backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export PORT=8081
python -m uvicorn src.main:app --host 0.0.0.0 --port 8081
```

Le backend sera disponible sur `http://localhost:8081`.

Si vous voyez encore une erreur du type `No module named 'structlog'`, vérifiez que vous utilisez bien le Python du venv :

```bash
which python
which uvicorn
python -m pip show structlog
```

Si `which uvicorn` pointe vers le Python système, lancez toujours `python -m uvicorn` comme ci-dessus.

## 2. Démarrer l'agent

Dans un deuxième terminal :

```bash
cd /Users/aksantibahiga/Documents/build_with_ai_workshop/agent
source .venv/bin/activate
export BACKEND_URL="http://localhost:8081"
cd matos
adk run .
```

L'agent utilise alors le backend local pour rechercher des produits et enregistrer les prospects.

Si `adk run .` prend du temps au premier démarrage, laissez-le finir ses imports. Si vous appuyez sur `Ctrl + C` pendant cette phase, vous pouvez voir un `KeyboardInterrupt` comme dans votre capture, ce qui signifie simplement que vous avez interrompu le lancement avant la fin.

## 3. Démarrer le bridge

Dans un troisième terminal :

```bash
cd /Users/aksantibahiga/Documents/build_with_ai_workshop/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export BACKEND_URL="http://localhost:8081"
export ADK_SERVICE_URL="http://localhost:8000"
export ADK_APP_NAME="matos"
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

Le bridge expose `POST /chat`, `POST /webhook/twilio` et `GET /health`.

Si vous obtenez cette erreur au démarrage du bridge : `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'`, voici deux possibilités :

1. Utiliser Python 3.10 ou plus récent pour le venv du bridge.
	- Vérifiez avec `python --version` dans le venv.
	- Si la version est trop ancienne, recréez le venv avec un Python plus récent, puis réinstallez les dépendances.

2. Remplacer les annotations `str | None` par `Optional[str]` dans `backend/src/config.py`.
	- Ajoutez `from typing import Optional`.
	- Remplacez `str | None` par `Optional[str]` pour `TWILIO_ACCOUNT_SID` et `TWILIO_AUTH_TOKEN`.
	- Cette option sert surtout si vous devez garder une version Python plus ancienne.

## 4. Démarrer le frontend

Dans un quatrième terminal :

```bash
cd /Users/aksantibahiga/Documents/build_with_ai_workshop/frontend
python3 -m http.server 5174
```

Ouvrez ensuite `http://localhost:5174`, puis utilisez `http://localhost:8000` comme URL du bridge.

## 5. Ordre recommandé

1. Lancez d'abord le backend local.
2. Lancez ensuite l'agent.
3. Lancez le bridge.
4. Ouvrez le frontend dans le navigateur.

Vous obtenez ainsi une chaîne complète locale : frontend -> bridge -> agent -> backend.

## 6. Prompts de test

Essayez ces messages dans le frontend ou via le bridge :

1. `Bonjour, je cherche un laptop`
2. `niko na tafuta machine ya 16go RAM`
3. `Je veux ce modèle, je m'appelle Amina, email amina@example.com`

## 7. Vérification rapide

Si quelque chose ne répond pas :

```bash
curl -fsS http://localhost:8081/health
curl -fsS http://localhost:8000/health
```

Si le backend ne démarre toujours pas, relancez son venv et réinstallez les dépendances avec `python -m pip install -r requirements.txt`.