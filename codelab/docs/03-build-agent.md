# 03 - Construire l'agent

Dans cette étape, vous validez le comportement de l'agent en local avant le déploiement.

## Résultat attendu

- `adk run .` fonctionne en local,
- les outils `search_products` et `save_customer_lead` fonctionnent,
- le comportement de repli est correct lorsqu'aucun produit exact n'est trouvé.

## 1. Préparer l'environnement local de l'agent

```bash
cd agent
[ -d venv ] || python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
adk --version
```

## 2. Confirmer la structure du package de l'agent

- `agent/matos/root_agent.py` contient la logique principale de l'agent.
- `agent/matos/__init__.py` exporte `root_agent`.

## 3. Lancer l'agent en local

```bash
export BACKEND_URL="$MATOS_BACKEND_URL"
cd matos
adk run .
```

## 4. Prompts de test rapide

Essayez ces exemples dans le CLI interactif :

1. `Hello, I need a laptop`
2. `niko na tafuta machine ya 16go RAM`
3. `I want a model that does not exist`
4. `I want this one, my name is Amina, email amina@example.com`

Utilisez `Ctrl + C` pour quitter.

## Vérification

Continuez lorsque :

- l'agent démarre sans erreur,
- la recherche de produits répond,
- le fallback fonctionne,
- la capture de lead réussit.

Important: au déploiement Cloud Run, `BACKEND_URL` doit être défini explicitement dans le service agent. L'étape 04 utilise `agent/deploy_agent.sh` pour forcer cette configuration et éviter les erreurs de type `Invalid URL '/products'`.

Suite : `04 - Deploy the Agent`
