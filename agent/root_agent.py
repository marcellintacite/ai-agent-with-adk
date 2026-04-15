"""
Matos Sales & Catalog AI Agent — Multilingual Edition
====================================================
A production-ready AI agent specialized in electronic products.
Connects directly to the Matos Cloud Run API for real-time inventory and lead capture.
"""

import os
import json
import logging
import requests
from typing import Optional
from dotenv import load_dotenv
from google.adk.agents import LlmAgent

# --- CONFIGURATION ---
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "https://matos-backend-742494222209.us-central1.run.app")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("matos_agent")

# --- TOOLS ---

def search_products(query: Optional[str] = None, category: Optional[str] = None) -> str:
    """
    Search the Matos catalog for electronics, laptops, or accessories.
    Recherche dans le catalogue Matos (ordinateurs, audio, accessoires).
    Tafuta kwenye katalogi ya Matos (kompyuta, vifaa vya kielektroniki).
    """
    try:
        params = {"q": query} if query else {}
        if category: params["category"] = category
        
        response = requests.get(f"{BACKEND_URL}/products", params=params, timeout=8)
        response.raise_for_status()
        products = response.json()
        
        if not products:
            return "No products found. / Aucun produit trouvé. / Hakuna bidhaa iliyopatikana."
            
        # Format for compact LLM consumption
        return "\n".join([
            f"- {p['name']} ({p['category']}): {p['price']} USD. Available: {p['available']}" 
            for p in products[:10]  # Return top 10 for efficiency
        ])
    except Exception as e:
        logger.error(f"Search error: {e}")
        return "Service temporarily unavailable. Please try again later."

def save_customer_lead(full_name: str, email: str, phone: Optional[str] = None) -> str:
    """
    Register a customer interested in buying a product.
    Enregistrer un client intéressé par un achat.
    Sajili mteja anayevutiwa na ununuzi.
    """
    try:
        payload = {"full_name": full_name, "email": email, "phone": phone}
        response = requests.post(f"{BACKEND_URL}/customers", json=payload, timeout=8)
        
        if response.status_code == 201:
            return "Customer successfully registered. / Client enregistré avec succès. / Mteja amesajiliwa vyema."
        elif response.status_code == 409:
            return "Email already exists in our system."
        return f"Error: {response.text}"
    except Exception as e:
        logger.error(f"Lead capture error: {e}")
        return "Failed to save contact. Please provide your info again."

# --- SYSTEM PROMPT ---

MATOS_INSTRUCTIONS = """
IDENTITY:
- You are 'Boutique Matos', the official AI for Matos, an electronics shop in DRC (Bukavu, Goma).
- You are professional, helpful, and multilingual (FR, SW, EN).

CORE RULES:
1. LANGUAGE: Always respond in the SAME LANGUAGE as the user (French or Swahili).
2. SALES: If the user searches for a product, show options. If they want to buy, use 'save_customer_lead'.
3. ACCURACY: Use 'search_products' for ANY product question. Do not invent products.
4. OUT OF STOCK: If a product is not available, suggest a similar category.

MASHARTI:
- JIBU KWA KISWAHILI ikiwa mtumiaji anauliza kwa Kiswahili.
- Ikiwa mteja anataka kununua, tumia 'save_customer_lead'.

CONSIGNES:
- RÉPONDS EN FRANÇAIS si l'utilisateur parle français.
- Propose d'enregistrer le client via 'save_customer_lead' dès qu'un intérêt d'achat est clair.
"""

# --- AGENT ---

root_agent = LlmAgent(
    name="matos_orchestrator",
    description="Multilingual sales assistant for Matos Electronics",
    instruction=MATOS_INSTRUCTIONS,
    tools=[search_products, save_customer_lead],
)
