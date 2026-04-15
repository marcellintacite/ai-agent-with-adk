# 03 - Construire l'agent (simple et guidé)

Dans cette etape, on prepare un agent separe qui va dialoguer avec les clients WhatsApp.

Idee cle: l'agent ne travaille pas "a l'aveugle". On lui donne des outils pour appeler votre backend et recuperer les vraies donnees.

## 1. Commencer avec le fichier de base

Ouvrez `agent/root_agent.py` et mettez ce code de depart (avec TODO):

```python
import os
import logging
import requests
from typing import Optional
from dotenv import load_dotenv
from google.adk.agents import LlmAgent

# --- CONFIGURATION ---
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "https://replace-me.run.app")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("matos_agent")


def search_products(query: Optional[str] = None, category: Optional[str] = None) -> str:
    """Rechercher les produits Matos depuis le backend."""
    # [TODO-1] Construire params avec query/category.
    # [TODO-2] Appeler GET {BACKEND_URL}/products.
    # [TODO-3] Retourner une liste lisible de produits.
    # [TODO-4] Gérer le cas liste vide et erreurs reseau.
    return "[TODO]"


def save_customer_lead(full_name: str, email: str, phone: Optional[str] = None) -> str:
    """Enregistrer un prospect interesse dans le backend."""
    # [TODO-5] Construire payload {full_name, email, phone}.
    # [TODO-6] Appeler POST {BACKEND_URL}/customers.
    # [TODO-7] Gérer 201 (succes), 409 (deja existant), autres cas.
    # [TODO-8] Gérer les erreurs reseau.
    return "[TODO]"


MATOS_INSTRUCTIONS = """
Tu es l'assistant de vente Matos (Bukavu).
- Reponds dans la meme langue que l'utilisateur (FR/SW/EN).
- Pour toute question produit/prix/disponibilite, appelle search_products.
- Si le client veut acheter, collecte nom + email (+ telephone optionnel), puis appelle save_customer_lead.
- N'invente jamais les produits.
"""


root_agent = LlmAgent(
    name="matos_orchestrator",
    description="Assistant de vente multilingue pour Matos",
    instruction=MATOS_INSTRUCTIONS,
    tools=[search_products, save_customer_lead],
)
```

## 2. Coller le code des TODO (copier-coller)

Dans `agent/root_agent.py`, remplacez chaque bloc TODO par le code suivant.

### TODO-1 a TODO-4 (fonction `search_products`, vers la ligne ~20)

```python
try:
    params = {}
    if query:
        params["q"] = query
    if category:
        params["category"] = category

    response = requests.get(f"{BACKEND_URL}/products", params=params, timeout=8)
    response.raise_for_status()
    products = response.json()

    if not products:
        return "Je ne trouve aucun produit pour cette recherche pour le moment."

    return "\n".join(
        [
            f"- {p['name']} ({p['category']}): {p['price']} USD. Disponible: {p['available']}"
            for p in products[:10]
        ]
    )
except Exception as e:
    logger.error(f"Search error: {e}")
    return "Service temporairement indisponible. Merci de reessayer."
```

### TODO-5 a TODO-8 (fonction `save_customer_lead`, vers la ligne ~40)

```python
try:
    payload = {"full_name": full_name, "email": email, "phone": phone}
    response = requests.post(f"{BACKEND_URL}/customers", json=payload, timeout=8)

    if response.status_code == 201:
        return "Parfait, vos informations ont ete enregistrees. Le proprietaire vous contactera bientot."
    if response.status_code == 409:
        return "Cet email existe deja dans le systeme."
    return f"Erreur backend: {response.text}"
except Exception as e:
    logger.error(f"Lead capture error: {e}")
    return "Impossible d'enregistrer vos informations maintenant. Merci de reessayer."
```

## 3. Test local rapide

```bash
cd agent
python3 -m py_compile root_agent.py
adk web
```

Essayez:

- `Avez-vous des laptops disponibles ?`
- `Nataka kununua laptop, naitwa Amina.`

Si tout est bon, passez a `04 - Deployer l'agent`.
