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
        temperature=0.8,
    )


def run_marketing_agent(state: dict) -> dict:
    business_type = state["business_type"]
    business_desc = state.get("business_desc", "")

    prompt = f"""You are a creative marketing strategist for a {business_type}.
Business: {business_desc}

Generate a concise marketing plan with:
1. **Campaign Theme**: One punchy campaign name and tagline (1 line each)
2. **Instagram Captions** (3 captions with emojis, each under 50 words)
3. **Promotional Ideas** (3 specific, actionable ideas for this business type)
4. **Best Marketing Channels** (top 3 with brief rationale)

Be specific to the {business_type} industry. Use Indian market context. Keep total response under 400 words. Format with clear headers."""

    response = invoke_with_retry(_get_llm(), [HumanMessage(content=prompt)])
    state["marketing_output"] = response.content
    return state
