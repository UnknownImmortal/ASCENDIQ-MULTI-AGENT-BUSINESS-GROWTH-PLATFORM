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


def run_support_agent(state: dict) -> dict:
    business_type = state["business_type"]
    business_desc = state.get("business_desc", "")

    prompt = f"""You are a customer experience specialist for a {business_type} in India.
Business: {business_desc}

Create:
1. **Top 5 FAQs** with concise, friendly answers (specific to {business_type})
2. **Complaint Response Templates** (2 templates: one for delay/quality issue, one for refund request)
3. **Proactive Support Tips** (3 ways to prevent common issues before they arise)
4. **Customer Delight Moment** (1 surprise & delight idea unique to {business_type})

Tone: warm, professional, Indian context. Under 400 words. Clear headers."""

    response = invoke_with_retry(_get_llm(), [HumanMessage(content=prompt)])
    state["support_output"] = response.content
    return state
