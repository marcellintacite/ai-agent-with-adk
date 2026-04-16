# 03 - Construire l'agent

## Ce que vous allez faire

Dans cette étape, vous préparez l'agent conversationnel qui interroge le backend produits et enregistre les prospects.

## Pourquoi c'est important

L'agent est la couche d'intelligence métier: il transforme une question WhatsApp en actions concrètes (recherche de produits, qualification client, capture de lead).

## Résultat attendu en fin d'étape

- L'agent démarre localement avec `adk run` (CLI).
- Les tools `search_products` et `save_customer_lead` sont opérationnels.
- L'agent sait proposer des alternatives au lieu de bloquer la conversation.

## 1. Préparer l'environnement local de l'agent

```bash
cd agent
```

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
adk --version
```

## 2. Vérifier la structure actuelle

Le projet utilise maintenant un package agent dédié:

- `agent/matos/root_agent.py` -> logique principale
- `agent/matos/__init__.py` -> export du `root_agent`

Travaillez principalement dans `agent/matos/root_agent.py`.

## 3. Comprendre les deux tools métier

### Tool 1: `search_products(query, category)`

Rôle:

- Rechercher les produits via le backend (`GET /products`)
- Filtrer par catégorie si besoin
- Retourner une réponse lisible pour le client

Comportement attendu:

- Si résultat trouvé: liste courte des meilleurs produits
- Si aucun résultat: fallback intelligent vers catégories disponibles
- Si backend indisponible: message d'erreur propre (pas de crash)

### Tool 2: `save_customer_lead(full_name, email, phone)`

Rôle:

- Enregistrer un prospect via `POST /customers`

Comportement attendu:

- `201`: confirmation de création
- `409`: email déjà existant
- erreurs réseau: message clair + logs

## 4. Comprendre le prompt système

Le prompt doit forcer ces règles:

- répondre dans la langue de l'utilisateur (FR/SW/EN)
- ne jamais inventer de produits
- toujours proposer des alternatives si une recherche échoue
- collecter nom + email avant enregistrement du lead

## 5. Tester localement (mode interactif)

Ici, nous utilisons le CLI ADK (pas `adk web`).

```bash
cd agent
```

```bash
source venv/bin/activate
```

```bash
export BACKEND_URL="$MATOS_BACKEND_URL"
```

```bash
cd matos
```

```bash
adk run .
```

Le terminal passe en mode conversation. Testez ces scénarios:

1. Recherche simple: `Bonjour, je cherche un laptop`
2. Recherche par specs: `niko na tafuta machine ya 16go RAM`
3. Fallback: `je veux un modèle qui n'existe pas`
4. Intention d'achat: `Je prends ce modèle, je m'appelle Amina, email amina@example.com`

Pour quitter le mode interactif, utilisez `Ctrl + C`.

## 6. Checkpoint de sortie

Avant de passer à l'étape 04:

- l'agent démarre sans erreur
- la recherche produit répond
- le fallback fonctionne
- la capture de lead répond correctement

Note: l'objectif ici est de valider la logique agent via CLI. Le mode UI n'est pas utilisé dans cette étape.

Passez à `04 - Déployer l'agent`.
