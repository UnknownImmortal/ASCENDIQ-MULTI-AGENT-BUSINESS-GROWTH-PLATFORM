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
        temperature=0.7,
    )


def run_lead_agent(state: dict) -> dict:
    business_type = state["business_type"]
    business_desc = state.get("business_desc", "")

    prompt = f"""You are a B2C lead generation expert for a {business_type} in India.
Business: {business_desc}

Generate:
1. **Top 3 Customer Personas** (name, age range, key trait, what they want)
2. **Lead Acquisition Strategies** (3 specific tactics for {business_type})
3. **Outreach Message Templates** (2 short WhatsApp/DM messages, ready to send)
4. **Retention Hook** (1 loyalty idea to keep customers coming back)

Be hyper-specific to {business_type}. Indian market context. Under 350 words. Clear headers."""

    response = invoke_with_retry(_get_llm(), [HumanMessage(content=prompt)])
    state["lead_output"] = response.content
    return state
