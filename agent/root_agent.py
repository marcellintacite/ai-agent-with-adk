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
