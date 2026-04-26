"""
╔══════════════════════════════════════════════════════════════════════════╗
║         GEOPOLITICAL RISK INTELLIGENCE DASHBOARD                        ║
║         Global Macro Trading Signal System                              ║
║         Author: Macro Quant Framework v1.0                              ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import feedparser
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="GeoRisk Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════════════════════
# THEME — Dark Sovereign (Navy × Gold × Crimson)
# ══════════════════════════════════════════════════════════════════════════════
BG        = "#06091a"
BG2       = "#0c1128"
BG3       = "#111830"
BORDER    = "#1e2d52"
BORDER2   = "#243460"
GOLD      = "#f5c518"
GOLD_DIM  = "#a88512"
RED       = "#e05252"
RED_DIM   = "#8b2222"
GREEN     = "#3ecf8e"
AMBER     = "#f5a623"
BLUE      = "#4a9eff"
WHITE     = "#dce3f0"
WHITE_DIM = "#8899bb"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,400;0,500;1,400&family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; }}

.stApp {{
    background: {BG};
    font-family: 'Inter', sans-serif;
    color: {WHITE};
}}

.block-container {{
    padding: 1.2rem 2rem 3rem 2rem !important;
    max-width: 100% !important;
}}

/* Scrollbar */
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: {BG}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER2}; border-radius: 2px; }}

/* Section labels */
.sec-label {{
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: {GOLD_DIM};
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid {BORDER};
}}

/* Cards */
.card {{
    background: {BG2};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 18px;
}}

.card-sm {{
    background: {BG2};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 6px;
}}

/* Market tiles */
.mkt-tile {{
    background: {BG2};
    border: 1px solid {BORDER};
    border-top: 2px solid {GOLD};
    border-radius: 6px;
    padding: 10px 8px;
    text-align: center;
    transition: border-color 0.2s;
}}

.mkt-tile:hover {{ border-color: {GOLD}; }}

.mkt-ticker {{
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    color: {WHITE_DIM};
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 4px;
}}

.mkt-price {{
    font-family: 'DM Mono', monospace;
    font-size: 15px;
    font-weight: 500;
    color: {WHITE};
    margin-bottom: 3px;
}}

.mkt-up {{ color: {RED}; font-size: 11px; font-weight: 600; }}
.mkt-dn {{ color: {GREEN}; font-size: 11px; font-weight: 600; }}
.mkt-flat {{ color: {WHITE_DIM}; font-size: 11px; }}

/* Alert boxes */
.alert {{
    border-radius: 6px;
    padding: 9px 14px;
    margin: 5px 0;
    font-size: 12.5px;
    font-weight: 500;
    line-height: 1.5;
    border-left: 3px solid;
}}
.alert-red    {{ background: rgba(224,82,82,0.10); border-left-color: {RED};   color: {WHITE}; }}
.alert-amber  {{ background: rgba(245,166,35,0.10); border-left-color: {AMBER}; color: {WHITE}; }}
.alert-green  {{ background: rgba(62,207,142,0.10); border-left-color: {GREEN}; color: {WHITE}; }}

/* Impact matrix rows */
.impact-row {{
    display: flex;
    align-items: center;
    background: {BG2};
    border: 1px solid {BORDER};
    border-radius: 7px;
    padding: 9px 14px;
    margin: 4px 0;
    gap: 10px;
}}

/* News items */
.news-item {{
    padding: 8px 12px;
    margin: 5px 0;
    background: {BG2};
    border-left: 3px solid;
    border-radius: 0 6px 6px 0;
    font-size: 12.5px;
    line-height: 1.5;
    color: {WHITE};
}}
.news-high {{ border-left-color: {RED}; }}
.news-med  {{ border-left-color: {AMBER}; }}
.news-low  {{ border-left-color: {GREEN}; }}

/* Score number */
.score-hero {{
    font-family: 'Syne', sans-serif;
    font-size: 80px;
    font-weight: 800;
    line-height: 1;
    text-align: center;
}}

/* Hide Streamlit chrome */
#MainMenu {{ visibility: hidden; }}
footer     {{ visibility: hidden; }}
header     {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: {BG2};
    border-right: 1px solid {BORDER};
}}

div[data-testid="stCheckbox"] label {{ color: {WHITE_DIM} !important; font-size: 13px; }}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS — Risk NLP Keywords
# ══════════════════════════════════════════════════════════════════════════════

HIGH_RISK_KEYWORDS = [
    "war", "invasion", "airstrike", "nuclear", "missile", "bomb", "troops",
    "military offensive", "conflict", "blockade", "coup", "genocide",
    "escalation", "crisis", "collapse", "default", "catastrophe", "attack",
    "explosion", "assassination", "terror", "hostages", "troops deployed",
    "naval blockade", "strait", "strait of hormuz", "red sea", "drone strike"
]

MED_RISK_KEYWORDS = [
    "sanction", "tariff", "trade war", "tension", "threat", "dispute",
    "protest", "unrest", "hostility", "provocation", "expulsion",
    "seized", "detained", "opposition", "instability", "embargo",
    "retaliation", "diplomatic", "expel", "recalled ambassador",
    "trade restriction", "market selloff", "recession", "stagflation"
]

LOW_RISK_KEYWORDS = [
    "ceasefire", "peace", "deal", "agreement", "resolution",
    "diplomacy", "negotiation", "withdraw", "de-escalate",
    "cooperation", "summit", "truce", "mediation", "stabilise"
]

RSS_FEEDS = [
    ("BBC World",    "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("Reuters",      "https://feeds.reuters.com/reuters/worldNews"),
    ("Al Jazeera",   "https://www.aljazeera.com/xml/rss/all.xml"),
    ("NYT World",    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"),
]

MARKET_TICKERS = {
    "Oil (WTI)": "CL=F",
    "Gold":      "GC=F",
    "US 10Y":    "^TNX",
    "VIX":       "^VIX",
    "DXY":       "DX-Y.NYB",
    "Bitcoin":   "BTC-USD",
    "S&P 500":   "^GSPC",
    "Silver":    "SI=F",
}


# ══════════════════════════════════════════════════════════════════════════════
# DATA LAYER — Fetchers (Cached)
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=300)
def fetch_market_data() -> dict:
    """Fetch live market data for all tracked instruments."""
    result = {}
    for label, ticker in MARKET_TICKERS.items():
        try:
            tk = yf.Ticker(ticker)
            data = tk.history(period="10d", interval="1d")
            if data.empty or len(data) < 2:
                continue
            closes = data["Close"].dropna()
            price_now = float(closes.iloc[-1])
            price_1d  = float(closes.iloc[-2])
            price_5d  = float(closes.iloc[max(0, len(closes) - 6)])
            chg_1d    = (price_now - price_1d) / price_1d * 100
            chg_5d    = (price_now - price_5d) / price_5d * 100
            result[label] = {
                "price":  price_now,
                "chg_1d": chg_1d,
                "chg_5d": chg_5d,
                "history": closes.tolist()[-10:],
            }
        except Exception:
            pass
    return result


@st.cache_data(ttl=900)
def fetch_historical_risk(days: int = 30) -> pd.DataFrame:
    """
    Reconstruct a market-derived risk score for the last N days.
    Uses VIX, Gold, Oil and DXY as inputs — no external DB required.
    """
    try:
        raw = {}
        for key, ticker in [("vix","^VIX"), ("gold","GC=F"),
                             ("oil","CL=F"), ("dxy","DX-Y.NYB")]:
            tk_data = yf.Ticker(ticker).history(period="40d", interval="1d")
            if not tk_data.empty:
                raw[key] = tk_data["Close"].dropna()

        if len(raw) < 2:
            return pd.DataFrame()

        df = pd.DataFrame(raw).dropna().iloc[-days:]

        scores, regimes = [], []
        for i in range(len(df)):
            v = float(df["vix"].iloc[i])
            g_chg = float(df["gold"].pct_change(5).iloc[i] * 100) if i >= 5 else 0.0
            o_chg = float(df["oil"].pct_change(5).iloc[i] * 100)  if i >= 5 else 0.0
            d_chg = float(df["dxy"].pct_change(5).iloc[i] * 100)  if i >= 5 else 0.0

            vix_s  = min(35, max(0.0, (v - 10) / 40 * 35))
            gold_s = min(20, max(0.0, g_chg * 4))  if g_chg > 0 else 0.0
            oil_s  = min(15, max(0.0, o_chg * 1.5)) if o_chg > 0 else 0.0
            dxy_s  = min(10, max(0.0, d_chg * 5))   if d_chg > 0 else 0.0

            total = min(100.0, vix_s + gold_s + oil_s + dxy_s)
            scores.append(total)

            if total >= 70:   regimes.append("EXTREME")
            elif total >= 50: regimes.append("ELEVATED")
            elif total >= 30: regimes.append("MODERATE")
            else:             regimes.append("LOW")

        df["risk_score"] = scores
        df["regime"]     = regimes
        return df[["risk_score", "regime"]]
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=600)
def fetch_news() -> list:
    """Fetch RSS news and score each headline for geopolitical risk."""
    articles = []
    for source, url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:12]:
                title   = entry.get("title",   "").strip()
                summary = entry.get("summary", "")[:250].strip()
                link    = entry.get("link",    "#")
                pub     = entry.get("published", "")

                text = (title + " " + summary).lower()

                high_hits = sum(1 for kw in HIGH_RISK_KEYWORDS if kw in text)
                med_hits  = sum(1 for kw in MED_RISK_KEYWORDS  if kw in text)
                low_hits  = sum(1 for kw in LOW_RISK_KEYWORDS  if kw in text)

                risk = min(1.0, (high_hits * 0.35 + med_hits * 0.15))
                risk -= low_hits * 0.08
                risk = max(0.0, risk)

                level = "high" if risk >= 0.35 else ("med" if risk >= 0.12 else "low")

                articles.append({
                    "source":  source,
                    "title":   title,
                    "summary": summary,
                    "link":    link,
                    "pub":     pub,
                    "risk":    risk,
                    "level":   level,
                })
        except Exception:
            pass

    return sorted(articles, key=lambda x: x["risk"], reverse=True)


# ══════════════════════════════════════════════════════════════════════════════
# RISK ENGINE — Scoring Model
# ══════════════════════════════════════════════════════════════════════════════

def compute_risk_score(market_data: dict, news: list) -> dict:
    """
    Composite Geopolitical Risk Score (0–100)

    MARKET SIGNALS (70 pts max):
      • VIX Fear Index         — 0 to 30 pts
      • Oil Price Shock        — 0 to 15 pts (geopolitical supply premium)
      • Gold Safe-Haven Flow   — 0 to 15 pts (crisis demand)
      • DXY Flight-to-Dollar   — 0 to 10 pts (EM stress / capital flight)

    NEWS SENTIMENT (30 pts max):
      • NLP keyword scoring of live RSS headlines
    """
    components = {}

    # ── VIX (0–30)
    vix = market_data.get("VIX", {}).get("price", 20.0)
    vix_s = min(30.0, max(0.0, (vix - 10) / 45 * 30))
    components["VIX Fear Index"]    = round(vix_s, 1)

    # ── Oil 5D spike (0–15)
    oil_5d = market_data.get("Oil (WTI)", {}).get("chg_5d", 0.0)
    oil_s  = min(15.0, max(0.0, oil_5d * 1.5)) if oil_5d > 0 else 0.0
    components["Oil Price Shock"]  = round(oil_s, 1)

    # ── Gold 5D safe-haven (0–15)
    gold_5d = market_data.get("Gold", {}).get("chg_5d", 0.0)
    gold_s  = min(15.0, max(0.0, gold_5d * 3.0)) if gold_5d > 0 else 0.0
    components["Gold Safe-Haven"]  = round(gold_s, 1)

    # ── DXY 5D flight-to-dollar (0–10)
    dxy_5d = market_data.get("DXY", {}).get("chg_5d", 0.0)
    dxy_s  = min(10.0, max(0.0, dxy_5d * 5.0)) if dxy_5d > 0 else 0.0
    components["USD Flight Safety"] = round(dxy_s, 1)

    # ── News sentiment (0–30)
    if news:
        risks = [a["risk"] for a in news[:25]]
        avg_risk = np.mean(risks) if risks else 0.12
        news_s = min(30.0, avg_risk * 70)
    else:
        news_s = 8.0   # baseline uncertainty
    components["News Sentiment"]    = round(news_s, 1)

    total = min(100.0, sum(components.values()))
    return {"total": round(total, 1), "components": components}


def get_regime(score: float) -> tuple:
    """Returns (label, color, bg_color) for score."""
    if score >= 70:
        return "EXTREME RISK-OFF",  RED,   "rgba(224,82,82,0.12)"
    elif score >= 50:
        return "ELEVATED RISK",     AMBER, "rgba(245,166,35,0.12)"
    elif score >= 30:
        return "MODERATE RISK",     GOLD,  "rgba(245,197,24,0.10)"
    else:
        return "LOW RISK / RISK-ON", GREEN, "rgba(62,207,142,0.10)"


def generate_alerts(score: float, market_data: dict) -> list:
    """Generate trading signals based on risk score and market conditions."""
    alerts = []

    if score >= 70:
        alerts += [
            ("red",   "🚨 RISK-OFF TRIGGERED — Cut equity exposure to 30–40% of book"),
            ("red",   "🥇 GOLD: Overweight immediately. Target 15–20% allocation"),
            ("red",   "📉 BONDS: Duration add — expect yield compression on flight-to-safety"),
            ("red",   "💵 DXY: Long USD. EM FX faces severe capital flight pressure"),
            ("amber", "⚡ HEDGE: Buy VIX calls or SPX put spreads. IV cheap vs realized"),
            ("amber", "🛢️ OIL: Monitor Hormuz/Red Sea disruption — supply shock premium"),
        ]
    elif score >= 50:
        alerts += [
            ("amber", "⚠️ Elevated geopolitical stress — trim equity risk incrementally"),
            ("amber", "🥇 GOLD: Begin accumulating. Safe-haven bid building structurally"),
            ("amber", "💵 DXY firm — avoid high-beta EM FX. INR/TRY/ZAR risk elevated"),
            ("amber", "📊 Reduce leverage. Use options to define risk on existing longs"),
            ("green", "✅ Maintain ~50% equity, 15% gold, 20% bonds, 15% cash"),
        ]
    elif score >= 30:
        alerts += [
            ("amber", "📊 Moderate risk — stay selective. Quality over high-beta"),
            ("green", "✅ Balanced book appropriate. Watch for score direction change"),
            ("green", "📈 No urgency to hedge — incremental position building OK"),
        ]
    else:
        alerts += [
            ("green", "✅ RISK-ON — Equity tailwinds present. Add cyclicals/growth"),
            ("green", "📈 EM markets: Strong entry. Capital flows turning positive"),
            ("green", "💎 Trim excess hedges. Selling vol is a viable strategy here"),
            ("green", "₿ Crypto: Risk-on regime historically supports BTC/ETH"),
        ]

    # Conditional market-specific signals
    vix = market_data.get("VIX", {}).get("price", 20)
    if vix > 40:
        alerts.append(("red", f"🔥 VIX={vix:.1f} — Capitulation zone. Consider mean-reversion long equities"))

    oil_1d = market_data.get("Oil (WTI)", {}).get("chg_1d", 0)
    if oil_1d > 3:
        alerts.append(("amber", f"🛢️ Oil +{oil_1d:.1f}% today — Supply shock. Long XLE/energy sector"))
    elif oil_1d < -3:
        alerts.append(("green", f"🛢️ Oil -{abs(oil_1d):.1f}% — Demand fear. Watch downstream relief"))

    gold_1d = market_data.get("Gold", {}).get("chg_1d", 0)
    if gold_1d > 1.5:
        alerts.append(("amber", f"🥇 Gold +{gold_1d:.1f}% — Safe-haven surge. Confirms risk-off thesis"))

    return alerts


def get_asset_impact(score: float) -> dict:
    """Maps risk score → directional signal per asset class."""
    if score >= 70:
        return {
            "Equities":    ("▼  SELL/REDUCE",    RED,   "Risk-off rotation. Cut to minimum weight. Hedge remaining longs."),
            "Gold":        ("▲  OVERWEIGHT",      GREEN, "Crisis demand. Central bank + institutional accumulation."),
            "Crude Oil":   ("▲  GEOPOLITICAL BID",AMBER, "Supply disruption premium. Long energy if Hormuz at risk."),
            "US Bonds":    ("▲  BUY DURATION",    GREEN, "Flight-to-safety crushes yields. Long TLT or ZN futures."),
            "USD (DXY)":   ("▲  STRONG BUY",      GREEN, "Global reserve rush. EM currencies face 3-7% correction."),
            "Bitcoin":     ("▼  SELL",             RED,   "Highly correlated with equities in panic episodes."),
            "EM / India":  ("▼  AVOID",            RED,   "Dual pressure: USD strength + FII outflows accelerating."),
        }
    elif score >= 50:
        return {
            "Equities":    ("→  TRIM / HEDGE",    AMBER, "Vol expanding. Reduce beta. Add SPX puts or collars."),
            "Gold":        ("▲  ACCUMULATE",       AMBER, "Structural safe-haven bid forming. Accumulate on dips."),
            "Crude Oil":   ("→  NEUTRAL / LONG",   AMBER, "Geopolitical premium forming. Watch supply data."),
            "US Bonds":    ("→  MILD BID",          AMBER, "Moderate safety flows. Curve flattening trade."),
            "USD (DXY)":   ("▲  FIRM",              AMBER, "EM FX under pressure. Avoid INR/BRL/ZAR exposure."),
            "Bitcoin":     ("→  REDUCE SIZE",       AMBER, "Volatile. Reduce position sizing, tighten stops."),
            "EM / India":  ("▼  DEFENSIVE",         AMBER, "FII outflow risk. Prefer domestic-oriented plays."),
        }
    elif score >= 30:
        return {
            "Equities":    ("→  SELECTIVE",        GOLD,  "Quality/value over growth. Keep leverage neutral."),
            "Gold":        ("→  HOLD",              GOLD,  "Maintain 5–8% as portfolio hedge. No urgency to add."),
            "Crude Oil":   ("→  FUNDAMENTALS",      GOLD,  "Supply/demand in focus. Geopolitical risk subdued."),
            "US Bonds":    ("→  NEUTRAL",            GOLD,  "Macro/rates dominant. Short duration bias."),
            "USD (DXY)":   ("→  BALANCED",           GOLD,  "Mixed flows. Watch Fed communication for direction."),
            "Bitcoin":     ("→  SPECULATIVE",        GOLD,  "Crypto-specific drivers. Only high-conviction trades."),
            "EM / India":  ("→  SELECTIVE",          GOLD,  "Country-specific alpha. India infra + domestic demand."),
        }
    else:
        return {
            "Equities":    ("▲  OVERWEIGHT",       GREEN, "Risk-on regime. Favor growth, cyclicals, small caps."),
            "Gold":        ("▼  TRIM",              RED,   "Opportunity cost too high. Reduce to 3–5% hedge."),
            "Crude Oil":   ("→  DEMAND-DRIVEN",     GREEN, "Inventory/demand dynamics. Not geopolitical."),
            "US Bonds":    ("▼  UNDERWEIGHT",       RED,   "Yields rising cycle. Stay short duration."),
            "USD (DXY)":   ("▼  WEAK BIAS",         RED,   "Risk-on = dollar selling. EM FX outperforms."),
            "Bitcoin":     ("▲  ACCUMULATE",        GREEN, "Risk-on regime historically drives crypto inflows."),
            "EM / India":  ("▲  OVERWEIGHT",        GREEN, "FII inflows. Strong entry for 6–12 month horizon."),
        }


# ══════════════════════════════════════════════════════════════════════════════
# VISUALIZATION — Charts
# ══════════════════════════════════════════════════════════════════════════════

def gauge_chart(score: float) -> go.Figure:
    regime, color, _ = get_regime(score)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 52, "color": color, "family": "DM Mono"},
            "suffix": "",
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": WHITE_DIM,
                "tickfont": {"color": WHITE_DIM, "size": 9, "family": "DM Mono"},
                "nticks": 6,
            },
            "bar":       {"color": color, "thickness": 0.22},
            "bgcolor":   BG3,
            "borderwidth": 0,
            "steps": [
                {"range": [0,  30],  "color": "rgba(62,207,142,0.08)"},
                {"range": [30, 50],  "color": "rgba(245,197,24,0.08)"},
                {"range": [50, 70],  "color": "rgba(245,166,35,0.09)"},
                {"range": [70, 100], "color": "rgba(224,82,82,0.12)"},
            ],
            "threshold": {
                "line":      {"color": color, "width": 3},
                "thickness": 0.82,
                "value":     score,
            },
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=230,
        margin=dict(t=20, b=10, l=20, r=20),
        font={"color": WHITE, "family": "Inter"},
    )
    return fig


def component_bar_chart(components: dict) -> go.Figure:
    labels = list(components.keys())
    values = list(components.values())
    bar_colors = [
        RED if v >= 20 else AMBER if v >= 10 else GOLD if v >= 5 else GREEN
        for v in values
    ]
    fig = go.Figure(go.Bar(
        x=values, y=labels,
        orientation="h",
        marker=dict(color=bar_colors, cornerradius=3),
        text=[f"{v:.1f}" for v in values],
        textposition="outside",
        textfont=dict(color=WHITE, size=10, family="DM Mono"),
        hovertemplate="%{y}: <b>%{x:.1f} pts</b><extra></extra>",
    ))
    max_val = max(values) if values else 30
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=185,
        margin=dict(t=5, b=5, l=5, r=40),
        xaxis=dict(
            range=[0, max_val + 6],
            showgrid=True, gridcolor=BORDER,
            tickfont=dict(color=WHITE_DIM, size=9, family="DM Mono"),
            title=dict(text="pts", font=dict(color=WHITE_DIM, size=9)),
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color=WHITE, size=10.5),
        ),
        bargap=0.35,
    )
    return fig


def historical_chart(hist_df: pd.DataFrame) -> go.Figure:
    if hist_df.empty:
        return go.Figure()

    scores = hist_df["risk_score"].values
    dates  = hist_df.index

    # Color each marker by regime
    marker_colors = []
    for s in scores:
        if s >= 70:   marker_colors.append(RED)
        elif s >= 50: marker_colors.append(AMBER)
        elif s >= 30: marker_colors.append(GOLD)
        else:         marker_colors.append(GREEN)

    fig = go.Figure()

    # Risk zone backgrounds
    for y0, y1, color in [
        (70, 100, f"rgba(224,82,82,0.06)"),
        (50, 70,  f"rgba(245,166,35,0.06)"),
        (30, 50,  f"rgba(245,197,24,0.05)"),
        (0,  30,  f"rgba(62,207,142,0.05)"),
    ]:
        fig.add_hrect(y0=y0, y1=y1, fillcolor=color, line_width=0)

    # Zone boundary lines
    for y, lbl, color in [
        (70, "EXTREME ≥70", RED),
        (50, "ELEVATED ≥50", AMBER),
        (30, "MODERATE ≥30", GOLD),
    ]:
        fig.add_hline(
            y=y, line=dict(color=color, width=0.5, dash="dot"),
            annotation_text=lbl,
            annotation_position="right",
            annotation_font=dict(color=color, size=8, family="DM Mono"),
        )

    # Score line + area
    fig.add_trace(go.Scatter(
        x=dates, y=scores,
        mode="lines+markers",
        line=dict(color=GOLD, width=2, shape="spline", smoothing=0.6),
        marker=dict(color=marker_colors, size=5, line=dict(width=0)),
        fill="tozeroy",
        fillcolor="rgba(245,197,24,0.05)",
        name="Risk Score",
        hovertemplate="<b>%{x|%b %d}</b><br>Score: <b>%{y:.1f}</b><extra></extra>",
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=190,
        margin=dict(t=10, b=30, l=45, r=80),
        yaxis=dict(
            range=[0, 100],
            showgrid=True, gridcolor=BORDER, gridwidth=0.5,
            tickfont=dict(color=WHITE_DIM, size=9, family="DM Mono"),
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color=WHITE_DIM, size=9),
        ),
        showlegend=False,
        hovermode="x unified",
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════════════════

def main():
    # ── Header ────────────────────────────────────────────────────────────────
    ts = datetime.utcnow().strftime("%a %d %b %Y  •  %H:%M UTC")
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:4px;">
        <div>
            <div style="font-family:'DM Mono',monospace; font-size:10px; color:{GOLD_DIM}; letter-spacing:3px; text-transform:uppercase; margin-bottom:2px;">
                Global Macro Intelligence System
            </div>
            <div style="font-family:'Syne',sans-serif; font-size:26px; font-weight:800; color:{WHITE}; line-height:1.1;">
                Geopolitical Risk Dashboard
            </div>
        </div>
        <div style="font-family:'DM Mono',monospace; font-size:11px; color:{WHITE_DIM}; text-align:right;">
            {ts}<br>
            <span style="color:{GOLD_DIM};">Live · Refreshes every 5 min</span>
        </div>
    </div>
    <hr style="border:none; border-top:1px solid {BORDER}; margin:10px 0 18px 0;">
    """, unsafe_allow_html=True)

    # ── Controls ──────────────────────────────────────────────────────────────
    ctrl1, ctrl2, ctrl3 = st.columns([1.2, 1, 6])
    with ctrl1:
        if st.button("⟳  Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    with ctrl2:
        auto = st.checkbox("Auto (5min)", value=False)

    # ── Fetch all data ────────────────────────────────────────────────────────
    with st.spinner("Connecting to market feeds..."):
        mkt   = fetch_market_data()
        news  = fetch_news()
        hist  = fetch_historical_risk(30)

    risk       = compute_risk_score(mkt, news)
    score      = risk["total"]
    components = risk["components"]
    regime, regime_color, regime_bg = get_regime(score)
    alerts     = generate_alerts(score, mkt)
    impact     = get_asset_impact(score)

    # ══════════════════════════════════════════════════════════════════════════
    # ROW 1 — Gauge | Components | Market Tiles
    # ══════════════════════════════════════════════════════════════════════════
    r1a, r1b, r1c = st.columns([2.2, 2.2, 5.6])

    with r1a:
        st.markdown(f'<div class="sec-label">Composite Risk Score</div>', unsafe_allow_html=True)
        st.plotly_chart(gauge_chart(score), use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"""
        <div style="text-align:center; margin-top:-8px;">
            <span style="background:{regime_bg}; color:{regime_color};
                  border:1px solid {regime_color}44; border-radius:4px;
                  padding:4px 14px; font-family:'DM Mono',monospace;
                  font-size:11px; font-weight:500; letter-spacing:1px;">
                {regime}
            </span>
        </div>
        """, unsafe_allow_html=True)

    with r1b:
        st.markdown(f'<div class="sec-label">Score Decomposition (pts)</div>', unsafe_allow_html=True)
        st.plotly_chart(component_bar_chart(components), use_container_width=True, config={"displayModeBar": False})
        total_mkt = sum(v for k, v in components.items() if k != "News Sentiment")
        news_comp = components.get("News Sentiment", 0)
        st.markdown(f"""
        <div style="display:flex; gap:8px; margin-top:2px;">
            <div style="flex:1; background:{BG2}; border:1px solid {BORDER}; border-radius:6px; padding:7px; text-align:center;">
                <div style="font-family:'DM Mono',monospace; font-size:18px; color:{GOLD}; font-weight:500;">{total_mkt:.0f}</div>
                <div style="font-size:9px; color:{WHITE_DIM}; letter-spacing:1px;">MKT SIGNALS</div>
            </div>
            <div style="flex:1; background:{BG2}; border:1px solid {BORDER}; border-radius:6px; padding:7px; text-align:center;">
                <div style="font-family:'DM Mono',monospace; font-size:18px; color:{AMBER}; font-weight:500;">{news_comp:.0f}</div>
                <div style="font-size:9px; color:{WHITE_DIM}; letter-spacing:1px;">NEWS RISK</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with r1c:
        st.markdown(f'<div class="sec-label">Live Market Snapshot</div>', unsafe_allow_html=True)
        tile_labels = list(MARKET_TICKERS.keys())
        cols = st.columns(len(tile_labels))

        for i, label in enumerate(tile_labels):
            with cols[i]:
                if label not in mkt:
                    st.markdown(f'<div class="mkt-tile"><div class="mkt-ticker">{label}</div><div class="mkt-flat">N/A</div></div>', unsafe_allow_html=True)
                    continue
                d = mkt[label]
                p = d["price"]
                c1 = d["chg_1d"]
                c5 = d["chg_5d"]

                # Format price
                if label == "Bitcoin":
                    p_str = f"${p:,.0f}"
                elif label == "S&P 500":
                    p_str = f"{p:,.0f}"
                elif label in ["US 10Y", "VIX", "DXY"]:
                    p_str = f"{p:.2f}"
                else:
                    p_str = f"${p:,.1f}"

                c1_str   = f"{'+'if c1>0 else ''}{c1:.1f}%"
                c5_str   = f"{'+'if c5>0 else ''}{c5:.1f}%"
                c1_class = "mkt-up" if c1 > 0 else ("mkt-dn" if c1 < 0 else "mkt-flat")

                st.markdown(f"""
                <div class="mkt-tile">
                    <div class="mkt-ticker">{label}</div>
                    <div class="mkt-price">{p_str}</div>
                    <div class="{c1_class}">{c1_str}</div>
                    <div style="font-size:10px; color:{WHITE_DIM};">5D {c5_str}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ROW 2 — Historical Chart | Trading Alerts
    # ══════════════════════════════════════════════════════════════════════════
    r2a, r2b = st.columns([5.5, 4.5])

    with r2a:
        st.markdown(f'<div class="sec-label">30-Day Risk Score History (Market-Derived)</div>', unsafe_allow_html=True)
        if not hist.empty:
            st.plotly_chart(historical_chart(hist), use_container_width=True, config={"displayModeBar": False})
            # Summary stats
            avg_s   = hist["risk_score"].mean()
            max_s   = hist["risk_score"].max()
            trend   = hist["risk_score"].iloc[-1] - hist["risk_score"].iloc[-5] if len(hist) >= 5 else 0
            t_dir   = f"↑ +{trend:.1f}" if trend > 0 else f"↓ {trend:.1f}"
            t_color = RED if trend > 0 else GREEN
            st.markdown(f"""
            <div style="display:flex; gap:8px; margin-top:4px;">
                <div class="card-sm" style="flex:1; text-align:center;">
                    <div style="font-family:'DM Mono',monospace; font-size:16px; color:{WHITE};">{avg_s:.1f}</div>
                    <div style="font-size:9px; color:{WHITE_DIM}; letter-spacing:1px;">30D AVG</div>
                </div>
                <div class="card-sm" style="flex:1; text-align:center;">
                    <div style="font-family:'DM Mono',monospace; font-size:16px; color:{RED};">{max_s:.1f}</div>
                    <div style="font-size:9px; color:{WHITE_DIM}; letter-spacing:1px;">30D HIGH</div>
                </div>
                <div class="card-sm" style="flex:1; text-align:center;">
                    <div style="font-family:'DM Mono',monospace; font-size:16px; color:{t_color};">{t_dir}</div>
                    <div style="font-size:9px; color:{WHITE_DIM}; letter-spacing:1px;">5D TREND</div>
                </div>
                <div class="card-sm" style="flex:1; text-align:center;">
                    <div style="font-family:'DM Mono',monospace; font-size:16px; color:{regime_color};">{score:.1f}</div>
                    <div style="font-size:9px; color:{WHITE_DIM}; letter-spacing:1px;">CURRENT</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Historical data unavailable. Check network connectivity.")

    with r2b:
        st.markdown(f'<div class="sec-label">⚡ Trading Signals & Portfolio Alerts</div>', unsafe_allow_html=True)
        cls_map = {"red": "alert-red", "amber": "alert-amber", "green": "alert-green"}
        for level, msg in alerts[:7]:
            cls = cls_map.get(level, "alert-green")
            st.markdown(f'<div class="alert {cls}">{msg}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ROW 3 — Asset Impact Matrix | Live News Feed
    # ══════════════════════════════════════════════════════════════════════════
    r3a, r3b = st.columns([4.5, 5.5])

    with r3a:
        st.markdown(f'<div class="sec-label">Asset Class Impact Matrix — Score: {score:.0f} / {regime}</div>', unsafe_allow_html=True)
        for asset, (signal, color, rationale) in impact.items():
            st.markdown(f"""
            <div class="impact-row">
                <div style="font-size:12.5px; font-weight:600; color:{WHITE}; min-width:90px;">{asset}</div>
                <div style="font-family:'DM Mono',monospace; font-size:11px; font-weight:500;
                            color:{color}; min-width:140px;">{signal}</div>
                <div style="font-size:11px; color:{WHITE_DIM}; flex:1; line-height:1.4;">{rationale}</div>
            </div>
            """, unsafe_allow_html=True)

    with r3b:
        st.markdown(f'<div class="sec-label">Live Geopolitical Intelligence Feed ({len(news)} headlines)</div>', unsafe_allow_html=True)
        if news:
            for art in news[:10]:
                lmap  = {"high": RED, "med": AMBER, "low": GREEN}
                lcolor = lmap.get(art["level"], WHITE_DIM)
                icon  = {"high": "🔴", "med": "🟡", "low": "🟢"}.get(art["level"], "⚪")
                risk_pct = int(art["risk"] * 100)
                title_short = art["title"][:95] + ("…" if len(art["title"]) > 95 else "")
                st.markdown(f"""
                <div class="news-item news-{art['level']}">
                    <div style="font-weight:600; color:{WHITE}; margin-bottom:3px; font-size:12.5px; line-height:1.4;">{title_short}</div>
                    <div style="display:flex; gap:10px; align-items:center; margin-top:3px;">
                        <span style="font-family:'DM Mono',monospace; font-size:9.5px; color:{lcolor}; font-weight:500;">
                            {icon} {art['level'].upper()} · {risk_pct}%
                        </span>
                        <span style="font-size:9px; color:{WHITE_DIM};">{art['source']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("News feeds unavailable. Check RSS sources or network config.")

    # ══════════════════════════════════════════════════════════════════════════
    # FOOTER — Methodology & Disclaimer
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="border-top:1px solid {BORDER}; padding-top:14px; font-size:11px; color:{WHITE_DIM}; line-height:1.8;">
        <span style="color:{GOLD}; font-weight:600; font-family:'DM Mono',monospace;">SCORE METHODOLOGY</span><br>
        <b>Market Signals (70 pts):</b>
        VIX Fear Index (0–30) + Oil Price Shock (0–15) + Gold Safe-Haven Flow (0–15) + USD Flight-to-Safety (0–10) &nbsp;|&nbsp;
        <b>News Sentiment (30 pts):</b> NLP keyword scoring across {len(RSS_FEEDS)} global RSS feeds.
        Score recomputes every 5 minutes. Historical reconstruction uses market signals only (news not archived).
        <br><span style="color:{RED_DIM};">⚠️ NOT financial advice. For research &amp; educational use only.
        Always verify with primary sources before trading.</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Auto refresh logic
    if auto:
        time.sleep(300)
        st.cache_data.clear()
        st.rerun()


if __name__ == "__main__":
    main()
