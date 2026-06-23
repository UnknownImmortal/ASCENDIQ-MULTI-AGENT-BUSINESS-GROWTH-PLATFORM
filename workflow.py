from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, List
from agents.marketing_agent import run_marketing_agent
from agents.lead_agent import run_lead_agent
from agents.support_agent import run_support_agent
from agents.inventory_agent import run_inventory_agent
from agents.analytics_agent import run_analytics_agent
from agents.report_agent import run_report_agent


class BusinessState(TypedDict):
    business_type: str
    business_desc: str
    kpis: dict
    low_stock: List[str]
    top_products: List[str]
    marketing_output: Optional[str]
    lead_output: Optional[str]
    support_output: Optional[str]
    inventory_output: Optional[str]
    analytics_output: Optional[str]
    report_output: Optional[str]


def build_workflow():
    graph = StateGraph(BusinessState)

    graph.add_node("marketing", run_marketing_agent)
    graph.add_node("lead_gen", run_lead_agent)
    graph.add_node("support", run_support_agent)
    graph.add_node("inventory", run_inventory_agent)
    graph.add_node("analytics", run_analytics_agent)
    graph.add_node("report", run_report_agent)

    graph.set_entry_point("marketing")
    graph.add_edge("marketing", "lead_gen")
    graph.add_edge("lead_gen", "support")
    graph.add_edge("support", "inventory")
    graph.add_edge("inventory", "analytics")
    graph.add_edge("analytics", "report")
    graph.add_edge("report", END)

    return graph.compile()


def run_full_analysis(business_type: str, business_data: dict) -> dict:
    workflow = build_workflow()
    
    initial_state: BusinessState = {
        "business_type": business_type,
        "business_desc": business_data.get("business_desc", ""),
        "kpis": business_data.get("kpis", {}),
        "low_stock": business_data.get("low_stock", []),
        "top_products": business_data.get("top_products", []),
        "marketing_output": None,
        "lead_output": None,
        "support_output": None,
        "inventory_output": None,
        "analytics_output": None,
        "report_output": None,
    }
    
    result = workflow.invoke(initial_state)
    return result
