import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import GEMINI_MODEL, invoke_with_retry
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


def _get_llm():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=api_key,
        temperature=0.5,
    )


def run_inventory_agent(state: dict) -> dict:
    business_type = state["business_type"]
    low_stock = state.get("low_stock", [])
    top_products = state.get("top_products", [])

    low_stock_str = ", ".join(low_stock) if low_stock else "None identified"
    products_str = ", ".join(top_products[:3]) if top_products else "key products"

    prompt = f"""You are an inventory and supply chain advisor for a {business_type} in India.

Current Status:
- Low Stock Items: {low_stock_str}
- Top Products: {products_str}

Provide:
1. **Reorder Recommendations** (specific quantities and urgency for each low-stock item)
2. **Demand Forecast** (next 30 days prediction for top 3 products, with reasoning)
3. **Waste Reduction Tips** (2-3 specific to {business_type})
4. **Supplier Negotiation Tip** (1 actionable advice for better pricing)
5. **Stock Optimization** (1 smart bundling or storage idea)

Be practical, numbers-driven, Indian supply chain context. Under 350 words. Clear headers."""

    response = invoke_with_retry(_get_llm(), [HumanMessage(content=prompt)])
    state["inventory_output"] = response.content
    return state
