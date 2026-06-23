# ASCENDIQ

> **Your AI Chief Growth Officer** — A premium multi-agent business intelligence platform for Indian SMEs.

Built with **LangGraph** + **Streamlit** for hackathons and MVPs.

---

## 🎯 What It Does

ASCENDIQ deploys **5 specialized AI agents** to analyze your business and generate actionable growth strategies:

| Agent | What It Does |
|-------|-------------|
| 📣 Marketing Agent | Social campaigns, Instagram captions, promo ideas |
| 🎯 Lead Gen Agent | Customer personas, acquisition tactics, outreach messages |
| 💬 Support Agent | FAQs, complaint templates, delight moments |
| 📦 Inventory Agent | Stock alerts, demand forecast, reorder recommendations |
| 📊 Analytics Agent | Insights, growth opportunities, risk alerts |
| 📋 CEO Report | Executive summary with health score & action plan |

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone <your-repo>
cd growthpilot
pip install -r requirements.txt
```

### 2. Get Gemini API Key

Visit [Google AI Studio](https://aistudio.google.com/app/apikey) and create a free API key.

### 3. Run

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🏗️ Project Structure

```
ascendiq/
├── app.py                    # Main Streamlit app
├── workflow.py               # LangGraph multi-agent workflow
├── requirements.txt
├── README.md
├── agents/
│   ├── marketing_agent.py    # Campaign & content generation
│   ├── lead_agent.py         # Lead generation & personas
│   ├── support_agent.py      # Customer support templates
│   ├── inventory_agent.py    # Stock management & forecasting
│   ├── analytics_agent.py    # Business intelligence
│   └── report_agent.py       # CEO executive report
├── data/
│   └── sample_data.py        # Mock data for 5 business types
├── utils/
│   ├── charts.py             # Plotly chart components
│   └── database.py           # SQLite for analysis history
└── assets/
    └── style.css             # Premium custom CSS
```

---

## 🎨 Design System

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#F8F5F0` | App background |
| Primary | `#1F4D3A` | Headers, CTAs |
| Accent | `#7A9E7E` | Labels, highlights |
| Surface | `#FFFFFF` | Cards |
| Border | `#E8E2D9` | Card borders |

---

## ☁️ Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → select `app.py`
4. Add secret: `GEMINI_API_KEY = "your-key"` in Streamlit Secrets
5. Deploy!

For Streamlit Secrets, update `app.py` to read:
```python
import streamlit as st
api_key = st.secrets.get("GEMINI_API_KEY", "")
```

---

## 🏆 Hackathon Notes

- **No auth** — runs instantly, zero friction
- **Mock data** — demo works without real business data  
- **Threaded agents** — progress bar shows live agent status
- **SQLite** — stores analysis history across sessions
- **Mobile responsive** — works on phones too

---

## 📦 Business Types Supported

- 🥐 **Bakery** — ₹75,000/mo revenue sample data
- ☕ **Café** — ₹1,20,000/mo revenue sample data  
- 💪 **Gym** — ₹90,000/mo revenue sample data
- 👗 **Clothing Store** — ₹2,10,000/mo revenue sample data
- 💼 **Freelance Agency** — ₹1,80,000/mo revenue sample data

---

Made with ❤️ for Indian SMEs · 
