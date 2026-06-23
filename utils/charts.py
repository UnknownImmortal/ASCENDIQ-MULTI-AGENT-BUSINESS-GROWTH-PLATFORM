import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

COLORS = {
    "primary": "#1F4D3A",
    "accent": "#7A9E7E",
    "accent_light": "#A8C5AB",
    "bg": "#F8F5F0",
    "surface": "#FFFFFF",
    "border": "#E8E2D9",
}

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#1A1A1A"),
    margin=dict(l=20, r=20, t=40, b=20),
)

def revenue_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df["Month"],
        y=df["Revenue (₹)"],
        fill="tozeroy",
        fillcolor="rgba(31,77,58,0.08)",
        line=dict(color=COLORS["primary"], width=3),
        mode="lines+markers",
        marker=dict(size=8, color=COLORS["primary"], 
                   line=dict(width=2, color="white")),
        hovertemplate="<b>%{x}</b><br>₹%{y:,}<extra></extra>"
    ))
    
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Revenue Trend", font=dict(size=15, color=COLORS["primary"]), x=0),
        xaxis=dict(showgrid=False, showline=False, tickfont=dict(size=12)),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)",
                   showline=False, tickformat="₹,.0f", tickfont=dict(size=11)),
        showlegend=False,
        height=280,
    )
    return fig


def customer_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df["Month"],
        y=df["Customers"],
        marker=dict(
            color=df["Customers"],
            colorscale=[[0, "#A8C5AB"], [1, "#1F4D3A"]],
            line=dict(width=0),
        ),
        hovertemplate="<b>%{x}</b><br>%{y} customers<extra></extra>",
        text=df["Customers"],
        textposition="outside",
        textfont=dict(size=11, color=COLORS["primary"]),
    ))
    
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Customer Growth", font=dict(size=15, color=COLORS["primary"]), x=0),
        xaxis=dict(showgrid=False, showline=False),
        yaxis=dict(showgrid=False, showline=False, visible=False),
        showlegend=False,
        height=280,
        bargap=0.3,
    )
    return fig


def demand_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    
    sorted_df = df.sort_values("Demand Score", ascending=True)
    
    fig.add_trace(go.Bar(
        x=sorted_df["Demand Score"],
        y=sorted_df["Product"],
        orientation="h",
        marker=dict(
            color=sorted_df["Demand Score"],
            colorscale=[[0, "#A8C5AB"], [1, "#1F4D3A"]],
            line=dict(width=0),
        ),
        hovertemplate="<b>%{y}</b><br>Score: %{x}<extra></extra>",
        text=sorted_df["Demand Score"],
        textposition="outside",
        textfont=dict(size=11),
    ))
    
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Product Demand Score", font=dict(size=15, color=COLORS["primary"]), x=0),
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(showgrid=False, showline=False, tickfont=dict(size=12)),
        showlegend=False,
        height=280,
    )
    return fig


def _donut_layout(title_text: str, margin_r: int = 140) -> dict:
    """Base layout for donut/pie charts — avoids conflict with CHART_LAYOUT margin."""
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#1A1A1A"),
        title=dict(text=title_text, font=dict(size=15, color=COLORS["primary"]), x=0),
        showlegend=True,
        legend=dict(orientation="v", x=1.02, y=0.5, font=dict(size=11), bgcolor="rgba(0,0,0,0)"),
        height=300,
        margin=dict(l=10, r=margin_r, t=40, b=10),
    )


def revenue_donut(df: pd.DataFrame) -> go.Figure:
    """Donut chart showing demand mix across top products."""
    fig = go.Figure(go.Pie(
        labels=df["Product"],
        values=df["Demand Score"],
        hole=0.62,
        marker=dict(colors=["#1F4D3A","#2D6B50","#7A9E7E","#A8C5AB","#C8DCC9"],
                    line=dict(color="#FFFFFF", width=2)),
        textinfo="label+percent",
        textfont=dict(size=11, family="Inter, sans-serif"),
        hovertemplate="<b>%{label}</b><br>Demand: %{value}<br>Share: %{percent}<extra></extra>",
        insidetextorientation="radial",
    ))
    fig.add_annotation(text="Demand<br>Mix", x=0.5, y=0.5,
                       font=dict(size=13, color=COLORS["primary"]), showarrow=False)
    fig.update_layout(**_donut_layout("Product Mix (Donut)", margin_r=120))
    return fig


def revenue_split_pie(kpis: dict, top_products: list) -> go.Figure:
    """Donut chart showing estimated revenue split by product."""
    weights = [35, 25, 20, 12, 8][:len(top_products)]
    total = sum(weights)
    values = [round(kpis["revenue"] * w / total) for w in weights]

    fig = go.Figure(go.Pie(
        labels=top_products[:len(weights)],
        values=values,
        hole=0.55,
        marker=dict(colors=["#1F4D3A","#2D6B50","#7A9E7E","#A8C5AB","#D4E8D5"],
                    line=dict(color="#FFFFFF", width=2)),
        textinfo="percent",
        textfont=dict(size=12, family="Inter, sans-serif"),
        hovertemplate="<b>%{label}</b><br>Est. Revenue: ₹%{value:,}<br>Share: %{percent}<extra></extra>",
    ))
    fig.add_annotation(
        text=f"₹{kpis['revenue']//1000}K<br>Total",
        x=0.5, y=0.5,
        font=dict(size=14, color=COLORS["primary"], family="Inter, sans-serif"),
        showarrow=False,
    )
    fig.update_layout(**_donut_layout("Est. Revenue by Product"))
    return fig


def customer_segment_donut(btype: str) -> go.Figure:
    """Donut chart of estimated customer segments per business type."""
    segments = {
        "Bakery":           (["Walk-ins", "Regulars", "Online Orders", "Events"],          [45, 35, 12, 8]),
        "Café":             (["Walk-ins", "Regulars", "Delivery", "Corporate"],             [40, 30, 20, 10]),
        "Gym":              (["Monthly Members", "Annual Members", "Personal Training", "Day Pass"], [50, 30, 12, 8]),
        "Clothing Store":   (["Walk-ins", "Repeat Buyers", "Online", "Referrals"],          [42, 28, 20, 10]),
        "Freelance Agency": (["Retainer Clients", "Project Clients", "Referrals", "New Leads"], [45, 30, 15, 10]),
    }
    labels, values = segments.get(btype, (["Direct", "Referral", "Online", "Other"], [40, 30, 20, 10]))

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.62,
        marker=dict(colors=["#1F4D3A","#7A9E7E","#A8C5AB","#D4E8D5"],
                    line=dict(color="#FFFFFF", width=2)),
        textinfo="percent",
        textfont=dict(size=12),
        hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
    ))
    fig.add_annotation(text="Customer<br>Segments", x=0.5, y=0.5,
                       font=dict(size=12, color=COLORS["primary"], family="Inter, sans-serif"),
                       showarrow=False)
    fig.update_layout(**_donut_layout("Customer Segments"))
    return fig


def gauge_chart(value: int, title: str) -> go.Figure:
    color = COLORS["primary"] if value >= 70 else ("#D97706" if value >= 50 else "#DC2626")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=dict(suffix="/100", font=dict(size=28, color=COLORS["primary"])),
        gauge=dict(
            axis=dict(range=[0, 100], tickwidth=0, tickcolor="#FFFFFF", showticklabels=False),
            bar=dict(color=color, thickness=0.6),
            bgcolor="rgba(0,0,0,0.04)",
            borderwidth=0,
            steps=[
                dict(range=[0, 50], color="rgba(220,38,38,0.08)"),
                dict(range=[50, 75], color="rgba(217,119,6,0.08)"),
                dict(range=[75, 100], color="rgba(22,163,74,0.08)"),
            ],
            threshold=dict(
                line=dict(color="rgba(0,0,0,0.2)", width=2),
                thickness=0.8,
                value=value
            )
        ),
        title=dict(text=title, font=dict(size=13, color=COLORS["accent"]))
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        margin=dict(l=20, r=20, t=30, b=10),
        height=180,
    )
    return fig
