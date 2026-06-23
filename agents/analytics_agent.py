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
        temperature=0.6,
    )


def run_analytics_agent(state: dict) -> dict:
    business_type = state["business_type"]
    kpis = state.get("kpis", {})

    revenue = kpis.get("revenue", 0)
    customers = kpis.get("customers", 0)
    growth_score = kpis.get("growth_score", 0)
    inventory_health = kpis.get("inventory_health", 0)

    prompt = f"""You are a business analytics expert reviewing a {business_type} in India.

Current Metrics:
- Monthly Revenue: ₹{revenue:,}
- Active Customers: {customers}
- Growth Score: {growth_score}/100
- Inventory Health: {inventory_health}/100

Provide:
1. **Business Health Assessment** (2-3 sentences, honest evaluation)
2. **Top 3 Growth Opportunities** (specific, actionable, ranked by impact)
3. **Top 3 Risk Alerts** (what could go wrong in next 90 days)
4. **Competitive Advantage** (what this {business_type} should double down on)
5. **90-Day Priority Actions** (3 specific steps with expected outcome)

Be data-driven, strategic, Indian SME context. Under 400 words. Clear headers."""

    response = invoke_with_retry(_get_llm(), [HumanMessage(content=prompt)])
    state["analytics_output"] = response.content
    return state
