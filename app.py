import streamlit as st
import os, sys, time, base64
sys.path.insert(0, os.path.dirname(__file__))

# Auto-load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv optional

from data.sample_data import get_business_df
from utils.charts import (
    revenue_chart, customer_chart, demand_chart,
    gauge_chart, revenue_split_pie, customer_segment_donut
)
from utils.database import save_analysis, get_recent_analyses

st.set_page_config(page_title="AscendIQ", page_icon="assets/favicon.png", layout="wide",
                   initial_sidebar_state="expanded")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

for k, v in [("page","landing"),("business_type",None),("analysis_result",None),
              ("gemini_key", os.environ.get("GEMINI_API_KEY","") or os.environ.get("GOOGLE_API_KEY","")),
              ("logged_in", False), ("user_name", ""), ("user_email", "")]:
    if k not in st.session_state:
        st.session_state[k] = v

# Load sidebar (white) logo as base64
with open("assets/logo_sidebar_base64.txt") as f:
    SIDEBAR_LOGO_B64 = f.read().strip()

# Push key to env in case loaded from .env
if st.session_state.gemini_key:
    os.environ["GEMINI_API_KEY"] = st.session_state.gemini_key
    os.environ["GOOGLE_API_KEY"] = st.session_state.gemini_key

BUSINESS_META = {
    "Bakery":           {"icon": "🥐", "emoji_html": "&#x1F950;", "desc": "Artisan breads & pastries"},
    "Café":             {"icon": "☕", "emoji_html": "&#x2615;",  "desc": "Specialty coffee & food"},
    "Gym":              {"icon": "💪", "emoji_html": "&#x1F4AA;", "desc": "Fitness & wellness"},
    "Clothing Store":   {"icon": "👗", "emoji_html": "&#x1F457;", "desc": "Fashion & accessories"},
    "Freelance Agency": {"icon": "💼", "emoji_html": "&#x1F4BC;", "desc": "Creative & digital services"},
}

BUSINESS_INSIGHTS = {
    "Bakery": {
        "quick_wins": [
            ("🎂", "Launch a weekend pre-order system for custom cakes — reduces waste and boosts guaranteed revenue by ~20%."),
            ("📱", "Post a 30-second 'morning bake' Reels video daily. Bakeries with behind-the-scenes content see 3× more walk-ins."),
            ("☕", "Bundle coffee + pastry combo at ₹99. Combos increase average order value by 35% in food businesses."),
        ],
        "watch_out": [
            ("⚠️", "Butter and flour prices spike in monsoon. Lock in supplier rates now for the next 3 months."),
            ("📉", "Weekend footfall drops if you don't post Friday reminders. Schedule posts every Thursday evening."),
        ],
        "owner_tip": "Your best customers are regulars who visit 3+ times a week. Give them a loyalty stamp card — free item every 10 visits. Retention is 5× cheaper than acquisition.",
        "this_week": ["Photograph your 3 best-selling items with natural light", "Message your top 20 customers a 'loyal customer' discount", "Add your bakery to Google Maps with photos and hours"],
    },
    "Café": {
        "quick_wins": [
            ("📸", "Create an 'Instagrammable corner' — a wall, neon sign, or flower shelf. Customers photograph it and tag you for free visibility."),
            ("🕐", "Introduce a 'Golden Hour' offer (2–4 PM) with 20% off. Fills dead hours and introduces new customers."),
            ("💻", "Market your café as a 'work-friendly' space with fast WiFi. Remote workers become loyal daily customers worth ₹3,000+/month each."),
        ],
        "watch_out": [
            ("⚠️", "Oat milk and specialty beans have long lead times. Keep 2-week buffer stock to avoid menu gaps."),
            ("📉", "Negative Google reviews drop foot traffic fast. Set a daily 5-minute alert to check and respond to all reviews."),
        ],
        "owner_tip": "Your top 10% of customers likely account for 40% of revenue. Know their names. Remember their order. That personal touch is something Starbucks can never replicate.",
        "this_week": ["Ask 5 happy customers to leave a Google review today", "Create a WhatsApp broadcast list of regulars for daily specials", "Test one new seasonal drink and announce it on Instagram Stories"],
    },
    "Gym": {
        "quick_wins": [
            ("👥", "Launch a 'Bring a Friend' week — friends work out free for 7 days. Conversion rate from trials is ~40% in fitness."),
            ("📊", "Offer free body composition analysis with a basic scale. It creates a data-driven reason for members to stay long-term."),
            ("🏆", "Run a 30-day transformation challenge with ₹500 entry fee and prizes. Creates community and drives consistency."),
        ],
        "watch_out": [
            ("⚠️", "January spike in memberships drops 60% by March. Lock new members into 3-month plans in January, not monthly."),
            ("📉", "Equipment downtime kills retention. Create a 'Report a broken machine' WhatsApp number and fix within 48 hours."),
        ],
        "owner_tip": "Most gym members quit not because of price, but because they stop seeing results. Assign every new member a check-in call at Week 2. That one call reduces churn by 25%.",
        "this_week": ["Post a member transformation story on Instagram (with permission)", "Call every member who hasn't visited in 14 days", "Create a beginner-friendly class schedule and share it on WhatsApp"],
    },
    "Clothing Store": {
        "quick_wins": [
            ("🎥", "Do a live 'New Stock Unboxing' on Instagram every time inventory arrives. Live shoppers buy 3× faster than browsing buyers."),
            ("💌", "Send a 'We saved this for you' WhatsApp message to top customers when new pieces arrive in their style/size."),
            ("🏷️", "Bundle slow-moving stock with bestsellers in a 'Curated Look' combo at 15% discount to clear inventory."),
        ],
        "watch_out": [
            ("⚠️", "Festival season inventory must be ordered 60 days in advance. Map out Diwali, Navratri, and wedding season now."),
            ("📉", "Size M and 8 are always first to run out. Keep 40% of stock in the most popular sizes, not split equally."),
        ],
        "owner_tip": "Your best marketing is a customer who walks out feeling amazing. Train your staff to genuinely compliment and suggest — not just sell. People return to stores where they feel good.",
        "this_week": ["Shoot a 60-second 'outfit of the day' Reel in your store", "Create a WhatsApp group for your top 30 customers for first-access drops", "Identify your 5 slowest-moving items and bundle them this week"],
    },
    "Freelance Agency": {
        "quick_wins": [
            ("📦", "Package your services into 3 clear tiers (Starter / Growth / Premium). Packaged pricing converts 2× better than custom quotes."),
            ("🤝", "Reach out to 5 complementary agencies for referral partnerships — share 10% referral fees."),
            ("📝", "Publish one case study per month with real numbers ('We grew their Instagram by 340% in 90 days')."),
        ],
        "watch_out": [
            ("⚠️", "Scope creep kills profitability. Use a simple change-request form for anything outside agreed deliverables."),
            ("📉", "Single large clients (>40% of revenue) are a risk. No client should exceed 25% of monthly billing."),
        ],
        "owner_tip": "Your existing clients are your easiest new revenue. Every 3 months, review what each client needs next and proactively pitch an upgrade or add-on. Upselling to happy clients costs nothing.",
        "this_week": ["Ask your 3 happiest clients for a LinkedIn recommendation today", "Write a one-paragraph case study for your best project", "Create a simple referral program: ₹2,000 credit for every referred client"],
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# LANDING PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def landing_page():
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-badge">✨ Powered by Gemini AI + LangGraph</div>
        <div class="hero-title">Your AI <span>Chief Growth Officer</span></div>
        <div class="hero-subtitle">
            Automate marketing, sales, support, and business decisions 
            with a team of five specialized AI agents — built for Indian SMEs.
        </div>
        <div class="hero-stats">
            <div class="hero-stat"><span class="hero-stat-number">5</span><span class="hero-stat-label">AI Agents</span></div>
            <div class="hero-stat"><span class="hero-stat-number">30s</span><span class="hero-stat-label">Full Analysis</span></div>
            <div class="hero-stat"><span class="hero-stat-number">5</span><span class="hero-stat-label">Business Types</span></div>
            <div class="hero-stat"><span class="hero-stat-number">∞</span><span class="hero-stat-label">Growth Potential</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-label">GET STARTED</div>
    <div class="section-title">Select Your Business Type</div>
    <div class="section-sub">Choose the category that best describes your business</div>
    """, unsafe_allow_html=True)

    cols = st.columns(5)
    for i, (btype, meta) in enumerate(BUSINESS_META.items()):
        with cols[i]:
            selected = st.session_state.business_type == btype
            card_class = "biz-card selected" if selected else "biz-card"
            st.markdown(f"""
            <div class="{card_class}">
                <span class="biz-icon">{meta['emoji_html']}</span>
                <div class="biz-name">{btype}</div>
                <div class="biz-desc">{meta['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Select", key=f"sel_{btype}", use_container_width=True):
                st.session_state.business_type = btype
                st.rerun()

    st.markdown('<div class="gp-divider"></div>', unsafe_allow_html=True)

    if st.session_state.business_type:
        meta = BUSINESS_META[st.session_state.business_type]
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="text-align:center;margin-bottom:20px;">
                <span class="info-pill">{meta['icon']} {st.session_state.business_type} selected</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚀 Launch GrowthPilot Dashboard", use_container_width=True, type="primary"):
                st.session_state.page = "dashboard"
                st.rerun()

    recent = get_recent_analyses(3)
    if recent:
        st.markdown('<div class="gp-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">RECENT ANALYSES</div>', unsafe_allow_html=True)
        cols = st.columns(len(recent))
        for i, (btype, ts) in enumerate(recent):
            with cols[i]:
                m = BUSINESS_META.get(btype, {"icon": "🏢"})
                st.markdown(f"""
                <div class="kpi-card" style="padding:16px;">
                    <div style="font-size:24px;">{m.get('icon','🏢')}</div>
                    <div style="font-size:14px;font-weight:600;color:var(--primary)">{btype}</div>
                    <div style="font-size:11px;color:var(--text-secondary)">{str(ts)[:16]}</div>
                </div>
                """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
def dashboard_page():
    btype = st.session_state.business_type
    meta = BUSINESS_META.get(btype, {"icon": "🏢", "desc": ""})
    biz_data = get_business_df(btype)
    kpis = biz_data["kpis"]
    insights = BUSINESS_INSIGHTS.get(btype, BUSINESS_INSIGHTS["Café"])

    # ── Header ─────────────────────────────────────────────────────────────────
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"""
        <div style="margin-bottom:24px;">
            <div class="section-label">BUSINESS DASHBOARD</div>
            <div class="section-title">{meta['icon']} {btype}</div>
            <div class="section-sub"><span class="status-dot"></span>Live data · Last updated just now</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("← Back", key="back_dash"):
            st.session_state.page = "landing"; st.rerun()

    # ── KPI Cards ──────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Monthly Revenue</div>
            <div class="kpi-value">₹{kpis['revenue']:,}</div>
            <div class="kpi-change">↑ 8.2% vs last month</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">👥</div>
            <div class="kpi-label">Active Customers</div>
            <div class="kpi-value">{kpis['customers']:,}</div>
            <div class="kpi-change">↑ 5.0% vs last month</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">📦</div>
            <div class="kpi-label">Inventory Health</div>
            <div class="kpi-value">{kpis['inventory_health']}%</div>
            <div class="kpi-change">{'✅ Healthy' if kpis['inventory_health'] >= 80 else '⚠️ Needs attention'}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">🚀</div>
            <div class="kpi-label">Growth Score</div>
            <div class="kpi-value">{kpis['growth_score']}/100</div>
            <div class="kpi-change">{'🔥 Strong' if kpis['growth_score'] >= 75 else '📈 Improving'}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Row 1: Line + Bar + Horizontal Bar ────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.plotly_chart(revenue_chart(biz_data["revenue_df"]),
                        use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.plotly_chart(customer_chart(biz_data["customer_df"]),
                        use_container_width=True, config={"displayModeBar": False})
    with c3:
        st.plotly_chart(demand_chart(biz_data["demand_df"]),
                        use_container_width=True, config={"displayModeBar": False})

    # ── Row 2: Two Donut Charts ────────────────────────────────────────────────
    st.markdown("""
    <div class="section-label" style="margin-top:8px;">DISTRIBUTION ANALYSIS</div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            revenue_split_pie(kpis, biz_data["top_products"]),
            use_container_width=True, config={"displayModeBar": False}
        )
    with c2:
        st.plotly_chart(
            customer_segment_donut(btype),
            use_container_width=True, config={"displayModeBar": False}
        )

    # ── Stock Alerts ───────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="agent-card">
        <div class="agent-header">
            <div class="agent-icon-wrap">⚠️</div>
            <div>
                <div class="agent-title">Stock Alerts</div>
                <div class="agent-subtitle">Items requiring immediate attention</div>
            </div>
        </div>
        <div>{''.join([f'<span class="alert-pill">🔴 {item}</span>' for item in biz_data["low_stock"]])}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gp-divider"></div>', unsafe_allow_html=True)

    # ── Insights & Advice ─────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="section-label">OWNER INTELLIGENCE</div>
    <div class="section-title">💡 Insights & Advice for Your {btype}</div>
    <div class="section-sub">Curated strategies and alerts tailored to your business type and current metrics</div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-tip-card">
        <div class="insight-tip-label">🧠 FOUNDER'S INSIGHT</div>
        <div class="insight-tip-text">{insights['owner_tip']}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        wins_html = "".join([
            f'<div class="insight-item insight-win"><span class="insight-icon">{icon}</span><span class="insight-text">{text}</span></div>'
            for icon, text in insights["quick_wins"]
        ])
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-icon-wrap">🚀</div>
                <div><div class="agent-title">Quick Wins</div>
                <div class="agent-subtitle">High-impact actions you can take this month</div></div>
            </div>
            <div class="insight-list">{wins_html}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        risks_html = "".join([
            f'<div class="insight-item insight-risk"><span class="insight-icon">{icon}</span><span class="insight-text">{text}</span></div>'
            for icon, text in insights["watch_out"]
        ])
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-icon-wrap">🔍</div>
                <div><div class="agent-title">Watch Out For</div>
                <div class="agent-subtitle">Risks specific to your business right now</div></div>
            </div>
            <div class="insight-list">{risks_html}</div>
        </div>
        """, unsafe_allow_html=True)

    checklist_html = "".join([
        f'<div class="checklist-item"><span class="check-box">☐</span><span class="check-text">{task}</span></div>'
        for task in insights["this_week"]
    ])
    st.markdown(f"""
    <div class="agent-card" style="margin-top:16px;">
        <div class="agent-header">
            <div class="agent-icon-wrap">📋</div>
            <div><div class="agent-title">Your Action Checklist — This Week</div>
            <div class="agent-subtitle">3 concrete steps to move the needle before Sunday</div></div>
        </div>
        <div class="checklist">{checklist_html}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gp-divider"></div>', unsafe_allow_html=True)

    # ── AI Agent CTA ──────────────────────────────────────────────────────────
    if not st.session_state.gemini_key:
        with st.expander("⚠️ Add your Gemini API key to unlock AI agents", expanded=False):
            st.markdown(
                'Get a free key at '
                '<a href="https://aistudio.google.com/app/apikey" target="_blank">aistudio.google.com</a>',
                unsafe_allow_html=True
            )
            cta_key = st.text_input("Gemini API Key", type="password",
                                    placeholder="AIza...", label_visibility="collapsed",
                                    key="dashboard_api_key_input")
            if cta_key:
                st.session_state.gemini_key = cta_key
                os.environ["GEMINI_API_KEY"] = cta_key
                os.environ["GOOGLE_API_KEY"] = cta_key
                st.rerun()

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🤖 Run Full AI Agent Analysis", use_container_width=True, type="primary"):
            st.session_state.page = "agents"; st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# AGENTS PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def agents_page():
    btype = st.session_state.business_type
    biz_data = get_business_df(btype)

    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown(f"""
        <div class="section-label">LANGGRAPH MULTI-AGENT WORKFLOW</div>
        <div class="section-title">🤖 AI Agent Analysis</div>
        <div class="section-sub">Five specialized agents analyzing your {btype} business</div>
        """, unsafe_allow_html=True)
    with c2:
        if st.button("← Dashboard", key="back_agents"):
            st.session_state.page = "dashboard"; st.rerun()

    st.markdown("""
    <div class="workflow-container">
        <div class="section-label" style="margin-bottom:16px;">AGENT PIPELINE</div>
        <div class="workflow-steps">
            <div class="workflow-step"><div class="step-bubble">🧠</div><div class="step-label">Business Input</div></div>
            <div class="step-arrow">→</div>
            <div class="workflow-step"><div class="step-bubble">📣</div><div class="step-label">Marketing</div></div>
            <div class="step-arrow">→</div>
            <div class="workflow-step"><div class="step-bubble">🎯</div><div class="step-label">Lead Gen</div></div>
            <div class="step-arrow">→</div>
            <div class="workflow-step"><div class="step-bubble">💬</div><div class="step-label">Support</div></div>
            <div class="step-arrow">→</div>
            <div class="workflow-step"><div class="step-bubble">📦</div><div class="step-label">Inventory</div></div>
            <div class="step-arrow">→</div>
            <div class="workflow-step"><div class="step-bubble">📊</div><div class="step-label">Analytics</div></div>
            <div class="step-arrow">→</div>
            <div class="workflow-step"><div class="step-bubble">📋</div><div class="step-label">CEO Report</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.analysis_result is None:
        # Ensure key is set in env before thread starts
        api_key = st.session_state.gemini_key or os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            st.error("⚠️ Gemini API key not found. Please add it to your `.env` file as `GEMINI_API_KEY=AIza...` and restart the app.")
            return
        os.environ["GEMINI_API_KEY"] = api_key
        os.environ["GOOGLE_API_KEY"] = api_key  # langchain-google-genai also checks this

        with st.spinner(""):
            progress_bar = st.progress(0)
            status_text = st.empty()
            agent_names = [
                "📣 Marketing Agent crafting campaigns...",
                "🎯 Lead Agent building customer personas...",
                "💬 Support Agent preparing FAQ responses...",
                "📦 Inventory Agent forecasting stock needs...",
                "📊 Analytics Agent generating insights...",
                "📋 Compiling CEO Executive Report...",
            ]
            try:
                from workflow import run_full_analysis
                import threading
                result_holder, error_holder = {}, {}
                _api_key = api_key  # capture for thread closure

                def run_analysis():
                    # Re-set in thread's env context to be safe
                    os.environ["GEMINI_API_KEY"] = _api_key
                    os.environ["GOOGLE_API_KEY"] = _api_key
                    try:
                        result_holder["result"] = run_full_analysis(btype, biz_data)
                    except Exception as e:
                        error_holder["error"] = str(e)
                        error_holder["type"] = type(e).__name__

                thread = threading.Thread(target=run_analysis)
                thread.start()
                step = 0
                while thread.is_alive():
                    status_text.markdown(
                        f"<div style='text-align:center;color:var(--primary);font-weight:500'>"
                        f"{agent_names[min(step, len(agent_names)-1)]}</div>",
                        unsafe_allow_html=True
                    )
                    progress_bar.progress(min(0.9, (step + 1) / len(agent_names)))
                    time.sleep(3); step += 1
                thread.join()

                if "error" in error_holder:
                    from config import GEMINI_MODEL
                    err_msg = error_holder["error"]
                    err_type = error_holder.get("type", "")

                    if err_type == "QuotaExceededError" or "RESOURCE_EXHAUSTED" in err_msg or "429" in err_msg:
                        st.warning(
                            "⏳ **Gemini API quota reached.** Your key has hit its free-tier limit "
                            "(some free keys allow as few as 20 requests/day — a full GrowthPilot run uses 6). "
                            "We already retried automatically; the quota is still exhausted right now."
                        )
                        st.markdown(
                            "**What to do:**\n"
                            "- Wait a bit (daily quotas usually reset at midnight Pacific time) and try again, or\n"
                            "- Use a different/paid Gemini API key with a higher quota — "
                            "[get or upgrade a key](https://aistudio.google.com/app/apikey)"
                        )
                    elif "NOT_FOUND" in err_msg or "404" in err_msg:
                        st.error(f"Agent error: {err_msg}")
                        st.warning(
                            f"⚠️ This app is configured to use model **`{GEMINI_MODEL}`**. "
                            f"If the error above mentions a different model name, your installed files are out of date — "
                            f"delete the project folder completely, re-extract a fresh copy, and clear any `__pycache__` folders before rerunning."
                        )
                    else:
                        st.error(f"Agent error: {err_msg}")
                    return

                progress_bar.progress(1.0)
                status_text.markdown("<div style='text-align:center;color:#16a34a;font-weight:600'>✅ Analysis complete!</div>",
                                     unsafe_allow_html=True)
                time.sleep(0.8)
                st.session_state.analysis_result = result_holder["result"]
                save_analysis(btype, result_holder["result"].get("report_output", "")[:300])
                st.rerun()
            except ImportError as e:
                st.error(f"Import error: {e}"); return

    if st.session_state.analysis_result:
        result = st.session_state.analysis_result
        tabs = st.tabs(["📣 Marketing", "🎯 Lead Gen", "💬 Support", "📦 Inventory", "📊 Analytics", "📋 CEO Report"])
        outputs = [
            ("marketing_output", "Marketing Agent",        "Campaigns, captions & promotional ideas", "📣"),
            ("lead_output",      "Lead Generation Agent",  "Personas, acquisition & outreach",        "🎯"),
            ("support_output",   "Customer Support Agent", "FAQs, responses & delight moments",       "💬"),
            ("inventory_output", "Inventory Agent",        "Stock alerts, forecast & recommendations","📦"),
            ("analytics_output", "Analytics Agent",        "Insights, opportunities & risks",         "📊"),
        ]
        for (key, title, subtitle, icon), tab in zip(outputs, tabs):
            with tab:
                output = result.get(key, "")
                if output:
                    st.markdown(f"""
                    <div class="agent-card">
                        <div class="agent-header">
                            <div class="agent-icon-wrap">{icon}</div>
                            <div><div class="agent-title">{title}</div>
                            <div class="agent-subtitle">{subtitle}</div></div>
                        </div>
                        <div class="agent-output">{output.replace(chr(10),'<br>')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Agent output not available.")

        with tabs[5]:
            report_output = result.get("report_output", "")
            kpis = biz_data["kpis"]
            st.markdown(f"""
            <div class="report-card">
                <div class="report-title">📋 Executive CEO Report</div>
                <div class="report-subtitle">GrowthPilot AI · {btype} Analysis · Confidential</div>
                <div style="display:flex;gap:24px;margin-bottom:24px;flex-wrap:wrap;">
                    <div><div class="health-score-ring">{kpis['growth_score']}</div></div>
                    <div style="flex:1">
                        <div style="font-size:13px;opacity:0.7;margin-bottom:4px">BUSINESS</div>
                        <div style="font-size:20px;font-weight:700">{btype}</div>
                        <div style="font-size:14px;opacity:0.7;margin-top:8px">Revenue: ₹{kpis['revenue']:,}/mo · {kpis['customers']} customers</div>
                    </div>
                </div>
                <div class="report-content">{report_output.replace(chr(10),'<br>') if report_output else 'Generating...'}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="gp-divider"></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("🔄 Run New Analysis", use_container_width=True):
                st.session_state.analysis_result = None
                st.session_state.page = "landing"; st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    with st.sidebar:
        # ── Logo (white version, fixed at top of sidebar — never scrolls) ──────
        st.markdown(f"""
        <div class="gp-sidebar-logo-wrap" id="gp-sidebar-logo">
            <img src="data:image/png;base64,{SIDEBAR_LOGO_B64}" alt="AscendIQ logo">
        </div>
        <div class="gp-sidebar-spacer"></div>
        <script>
        (function() {{
            function syncLogoWidth() {{
                const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
                const logo = window.parent.document.getElementById('gp-sidebar-logo');
                if (sidebar && logo) {{
                    logo.style.width = sidebar.getBoundingClientRect().width + 'px';
                }}
            }}
            syncLogoWidth();
            // Re-sync on window resize and when sidebar is manually dragged
            window.parent.addEventListener('resize', syncLogoWidth);
            const sidebarEl = window.parent.document.querySelector('[data-testid="stSidebar"]');
            if (sidebarEl && window.parent.ResizeObserver) {{
                new window.parent.ResizeObserver(syncLogoWidth).observe(sidebarEl);
            }}
        }})();
        </script>
        """, unsafe_allow_html=True)

        # ── Login / Sign Up Section ──────────────────────────────────────────────
        if not st.session_state.logged_in:
            auth_tab1, auth_tab2 = st.tabs(["Sign In", "Sign Up"])

            with auth_tab1:
                login_email = st.text_input("Email", placeholder="you@business.com",
                                            label_visibility="collapsed", key="login_email_input")
                login_pw = st.text_input("Password", placeholder="Password", type="password",
                                         label_visibility="collapsed", key="login_pw_input")
                if st.button("Sign In", use_container_width=True, type="primary", key="signin_btn"):
                    if login_email and login_pw:
                        st.session_state.logged_in = True
                        st.session_state.user_name = login_email.split("@")[0].title()
                        st.session_state.user_email = login_email
                        st.rerun()
                    else:
                        st.warning("Enter your email and password.")

            with auth_tab2:
                signup_name = st.text_input("Name", placeholder="Your name",
                                            label_visibility="collapsed", key="signup_name_input")
                signup_email = st.text_input("Email ", placeholder="you@business.com",
                                             label_visibility="collapsed", key="signup_email_input")
                signup_pw = st.text_input("Password ", placeholder="Create a password", type="password",
                                          label_visibility="collapsed", key="signup_pw_input")
                if st.button("Create Account", use_container_width=True, type="primary", key="signup_btn"):
                    if signup_name and signup_email and signup_pw:
                        st.session_state.logged_in = True
                        st.session_state.user_name = signup_name
                        st.session_state.user_email = signup_email
                        st.rerun()
                    else:
                        st.warning("Fill in all fields to create an account.")
        else:
            initials = "".join([w[0].upper() for w in st.session_state.user_name.split()[:2]]) or "U"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                <div style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.15);
                            display:flex;align-items:center;justify-content:center;font-size:14px;
                            font-weight:700;color:white;flex-shrink:0;">{initials}</div>
                <div style="overflow:hidden;">
                    <div style="font-size:13px;font-weight:600;color:white;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{st.session_state.user_name}</div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.55);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{st.session_state.user_email}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Sign Out", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user_name = ""
                st.session_state.user_email = ""
                st.rerun()

        st.markdown("---")

        # ── Navigation ──────────────────────────────────────────────────────────
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "landing"; st.rerun()
        if st.session_state.business_type:
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.page = "dashboard"; st.rerun()
            if st.session_state.analysis_result:
                if st.button("🤖 Agent Results", use_container_width=True):
                    st.session_state.page = "agents"; st.rerun()
        st.markdown("---")
        st.markdown("""
        <div style="font-size:12px;color:rgba(255,255,255,0.5);line-height:1.8;">
            <div style="margin-bottom:8px;font-weight:600;color:rgba(255,255,255,0.7)">AI AGENTS</div>
            📣 Marketing<br>🎯 Lead Generation<br>💬 Customer Support<br>📦 Inventory<br>📊 Analytics<br>📋 CEO Report
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div style="font-size:11px;color:rgba(255,255,255,0.4);">Built with LangGraph + Gemini<br>🏆 Hackathon MVP</div>',
                    unsafe_allow_html=True)

    page = st.session_state.page
    if page == "dashboard":
        dashboard_page()
    elif page == "agents":
        agents_page()
    else:
        landing_page()


if __name__ == "__main__":
    main()
