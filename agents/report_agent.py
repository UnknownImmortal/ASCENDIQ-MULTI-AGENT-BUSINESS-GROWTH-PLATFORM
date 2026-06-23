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


def run_report_agent(state: dict) -> dict:
    business_type = state["business_type"]
    kpis = state.get("kpis", {})

    revenue = kpis.get("revenue", 0)
    growth_score = kpis.get("growth_score", 0)

    marketing = state.get("marketing_output", "")[:300]
    leads = state.get("lead_output", "")[:300]
    analytics = state.get("analytics_output", "")[:300]

    prompt = f"""You are a Chief Strategy Officer writing an executive board report for a {business_type}.

Business Metrics:
- Revenue: ₹{revenue:,}/month
- Growth Score: {growth_score}/100

Agent Insights Summary:
- Marketing: {marketing}
- Customer Acquisition: {leads}
- Analytics: {analytics}

Write a concise EXECUTIVE REPORT with:
1. **Executive Summary** (3 sentences max — state of the business)
2. **Business Health Score**: X/100 with one-line justification
3. **Top 3 Opportunities** (bullet points, specific and numbered)
4. **Top 3 Risks** (bullet points, specific)
5. **CEO's 3 Recommended Actions** (immediate, 30-day, 90-day)
6. **Closing Verdict** (1 bold, confident statement about this business's trajectory)

Tone: Confident, board-room ready, data-backed. Under 400 words."""

    response = invoke_with_retry(_get_llm(), [HumanMessage(content=prompt)])
    state["report_output"] = response.content
    return state
