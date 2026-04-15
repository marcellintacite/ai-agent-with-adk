import os
import logging
import requests
from typing import Optional
from dotenv import load_dotenv
from google.adk.agents import LlmAgent

# --- CONFIGURATION ---
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "https://matos-backend-d3hu3ltnha-bq.a.run.app")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("matos_agent")

def search_products(query: Optional[str] = None, category: Optional[str] = None) -> str:
    """Rechercher les produits Matos depuis le backend.
    
    Supports:
    - query: Search by product name/description
    - category: Filter by category (e.g., 'laptops', 'smartphones')
    - Returns available categories if no match found
    """
    try:
        params = {}
        if query:
            params["q"] = query
        if category:
            params["category"] = category

        url = f"{BACKEND_URL}/products"
        params["available"] = "true"
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        products = response.json()

        if not products and not category:
            try:
                cat_response = requests.get(f"{BACKEND_URL}/products/categories", timeout=5)
                cat_response.raise_for_status()
                categories = cat_response.json().get("categories", [])
                if categories:
                    return f"Je n'ai pas trouvé de produit pour votre recherche. Voici les catégories disponibles: {', '.join(categories)}. Quelle catégorie vous intéresse?"
            except Exception:
                pass
            return "Je n'ai pas trouvé de produit correspondant. Pourriez-vous préciser votre recherche?"

        if products:
            formatted = []
            for product in products[:5]:
                formatted.append(
                    f"• {product['name']} ({product['category']}) - {product['price']} {product['currency']}"
                )
            return "\n".join(formatted)

        return "Aucun produit trouvé pour cette recherche."

    except requests.exceptions.Timeout:
        logger.error("Timeout calling backend products endpoint")
        return "Je ne peux pas accéder au catalogue en ce moment. Veuillez réessayer."
    except Exception as exc:
        logger.error(f"Error searching products: {exc}")
        return "Une erreur est survenue lors de la recherche. Veuillez réessayer."

def save_customer_lead(full_name: str, email: str, phone: Optional[str] = None) -> str:
    """Enregistrer un prospect interesse dans le backend."""
    try:
        payload = {
            "full_name": full_name.strip(),
            "email": email.strip(),
        }
        if phone:
            payload["phone"] = phone.strip()

        response = requests.post(f"{BACKEND_URL}/customers", json=payload, timeout=5)

        if response.status_code == 201:
            customer = response.json()
            logger.info(f"Customer created: {customer['email']}")
            return f"Merci! Votre demande a été enregistrée (ID: {customer['id']}). Nous vous recontacterons bientôt."
        if response.status_code == 409:
            logger.warning(f"Customer already exists: {email}")
            return f"Cet email ({email}) est déjà enregistré. Nous reviendrons vers vous."

        error_detail = response.json().get("detail", "Unknown error")
        logger.error(f"Customer creation failed: {error_detail}")
        return "Une erreur est survenue lors de l'enregistrement. Veuillez réessayer."

    except requests.exceptions.Timeout:
        logger.error("Timeout calling backend customers endpoint")
        return "Je ne peux pas enregistrer votre demande en ce moment. Veuillez réessayer."
    except Exception as exc:
        logger.error(f"Error saving customer: {exc}")
        return "Une erreur est survenue. Veuillez réessayer."

MATOS_INSTRUCTIONS = """
Tu es l'assistant de vente Matos (Bukavu) - un expert en électronique et ventes.

LANGUES: Reponds TOUJOURS dans la meme langue que l'utilisateur (FR/SW/EN). Pas de melange.

EXPERTISE:
- Tu connais notre catalogue complet: ordinateurs portables, smartphones, et autres electroniques.
- Categories disponibles: laptops, smartphones, tablets, etc.
- Tu es un CONSEILLER expert, pas un simple rechercheur.

STRATEGY POUR LES CLIENTS:
1. Si le client demande un produit SPECIFIQUE (ex: "HP EliteBook"), cherche-le d'abord.
   - Si trouve: presente le produit avec prix et specs
   - Si PAS trouve: Dis "Nous n'avons pas ce modele exact, mais nous avons des alternatives excellentes:" puis cherche dans la meme category (ex: category=laptops)

2. Si le client demande une CATEGORY (ex: "Je cherche un PC"), cherche par category=laptops.

3. Si le client refuse une proposition, PIVOT: "Quelle marque preferez-vous? Quel budget?"

4. JAMAIS dire "Je n'ai rien" - dire plutot "Voici ce que nous avons d'excellent"

REGLES POUR SEARCH_PRODUCTS:
- Utilise le parametre 'query' pour rechercher par nom/marque
- Si query ne retourne rien, cherche par 'category' pour proposer des alternatives
- Toujours privilege les produits disponibles (filtre automatique)
- Max 5 produits a la fois (ne pas surcharger l'utilisateur)

PARCOURS DE VENTE:
1. Ecoute et comprends le besoin du client
2. Propose les meilleur produits pour son besoin
3. Si le client s'interesse:
   - Collecte son NOM complet
   - Collecte son EMAIL (fondamental!)
   - Collecte son TELEPHONE (optional)
   - Appelle save_customer_lead
   - Confirme: "Merci! Nous vous recontacterons bientot"

REGLES IMPORTANTES:
- N'invente JAMAIS les produits - utilise TOUJOURS search_products
- Si backend indisponible, dis: "Je ne peux pas acceder au catalogue en ce moment, reessayez."
- Sois sympathique, aide-le a trouver ce qu'il cherche
- Pose des questions pour affiner: "Quel budget? Quelle utilisation?"
"""

root_agent = LlmAgent(
    name="matos_orchestrator",
    description="Assistant de vente multilingue pour Matos",
    instruction=MATOS_INSTRUCTIONS,
    tools=[search_products, save_customer_lead],
)
