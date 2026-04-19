import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cipher · Crypto Signals",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Coin Registry ────────────────────────────────────────────────────────────
COINS = {
    "BTC":  {"name": "Bitcoin",       "symbol": "BTCUSDT",  "icon": "₿",  "color": "#F7931A"},
    "ETH":  {"name": "Ethereum",      "symbol": "ETHUSDT",  "icon": "Ξ",  "color": "#627EEA"},
    "BNB":  {"name": "BNB",           "symbol": "BNBUSDT",  "icon": "⬡",  "color": "#F3BA2F"},
    "SOL":  {"name": "Solana",        "symbol": "SOLUSDT",  "icon": "◎",  "color": "#9945FF"},
    "XRP":  {"name": "XRP",           "symbol": "XRPUSDT",  "icon": "✕",  "color": "#00AAE4"},
    "ADA":  {"name": "Cardano",       "symbol": "ADAUSDT",  "icon": "₳",  "color": "#0D1E2D"},
    "DOGE": {"name": "Dogecoin",      "symbol": "DOGEUSDT", "icon": "Ð",  "color": "#C2A633"},
    "AVAX": {"name": "Avalanche",     "symbol": "AVAXUSDT", "icon": "▲",  "color": "#E84142"},
    "DOT":  {"name": "Polkadot",      "symbol": "DOTUSDT",  "icon": "●",  "color": "#E6007A"},
    "MATIC":{"name": "Polygon",       "symbol": "MATICUSDT","icon": "⬟",  "color": "#8247E5"},
    "LINK": {"name": "Chainlink",     "symbol": "LINKUSDT", "icon": "⬡",  "color": "#375BD2"},
    "UNI":  {"name": "Uniswap",       "symbol": "UNIUSDT",  "icon": "🦄", "color": "#FF007A"},
    "ATOM": {"name": "Cosmos",        "symbol": "ATOMUSDT", "icon": "⚛",  "color": "#2E3148"},
    "LTC":  {"name": "Litecoin",      "symbol": "LTCUSDT",  "icon": "Ł",  "color": "#BFBBBB"},
    "NEAR": {"name": "NEAR Protocol", "symbol": "NEARUSDT", "icon": "Ⓝ",  "color": "#00C08B"},
    "APT":  {"name": "Aptos",         "symbol": "APTUSDT",  "icon": "◈",  "color": "#00C8FF"},
    "ARB":  {"name": "Arbitrum",      "symbol": "ARBUSDT",  "icon": "⬡",  "color": "#12AAFF"},
    "OP":   {"name": "Optimism",      "symbol": "OPUSDT",   "icon": "✦",  "color": "#FF0420"},
    "SUI":  {"name": "Sui",           "symbol": "SUIUSDT",  "icon": "◆",  "color": "#6FBCF0"},
    "INJ":  {"name": "Injective",     "symbol": "INJUSDT",  "icon": "⬡",  "color": "#00B2FF"},
    "TRX":  {"name": "TRON",          "symbol": "TRXUSDT",  "icon": "◈",  "color": "#EF0027"},
    "XLM":  {"name": "Stellar",       "symbol": "XLMUSDT",  "icon": "✦",  "color": "#3E1BDB"},
    "FIL":  {"name": "Filecoin",      "symbol": "FILUSDT",  "icon": "⬡",  "color": "#0090FF"},
    "SAND": {"name": "The Sandbox",   "symbol": "SANDUSDT", "icon": "⬡",  "color": "#04ADEF"},
    "MANA": {"name": "Decentraland",  "symbol": "MANAUSDT", "icon": "⬡",  "color": "#FF2D55"},
}

# ─── Premium CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-primary: #000000;
    --bg-card: #0f0f0f;
    --bg-card2: #141414;
    --border: rgba(255,255,255,0.07);
    --border-bright: rgba(255,255,255,0.13);
    --accent-blue: #0A84FF;
    --accent-blue-dim: rgba(10,132,255,0.14);
    --accent-green: #30D158;
    --accent-green-dim: rgba(48,209,88,0.12);
    --accent-red: #FF453A;
    --accent-red-dim: rgba(255,69,58,0.12);
    --accent-amber: #FFD60A;
    --accent-amber-dim: rgba(255,214,10,0.10);
    --text-primary: rgba(255,255,255,0.93);
    --text-secondary: rgba(255,255,255,0.45);
    --text-tertiary: rgba(255,255,255,0.22);
    --font: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --mono: 'JetBrains Mono', monospace;
}
* { box-sizing: border-box; }
html, body, .stApp { background: var(--bg-primary) !important; font-family: var(--font) !important; color: var(--text-primary) !important; }
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }
h1,h2,h3,h4,h5,h6,p,span,div,label { font-family: var(--font) !important; -webkit-font-smoothing: antialiased; }

/* NAV */
.cipher-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 40px; height: 62px;
    border-bottom: 1px solid var(--border);
    background: rgba(0,0,0,0.85); backdrop-filter: blur(24px);
    position: sticky; top: 0; z-index: 100;
}
.cipher-logo { display:flex; align-items:center; gap:10px; font-size:17px; font-weight:650; letter-spacing:-0.4px; }
.cipher-logo-icon { width:30px; height:30px; background:var(--accent-blue); border-radius:7px; display:flex; align-items:center; justify-content:center; font-size:15px; }
.nav-right { display:flex; align-items:center; gap:16px; }
.live-pill { display:flex; align-items:center; gap:6px; background:var(--accent-green-dim); border:1px solid rgba(48,209,88,0.22); border-radius:20px; padding:5px 13px; font-size:11.5px; font-weight:600; color:var(--accent-green); }
.live-dot { width:6px; height:6px; border-radius:50%; background:var(--accent-green); animation:pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.35;transform:scale(0.75)} }
.nav-time { font-size:11px; font-family:var(--mono)!important; color:var(--text-tertiary); }

/* PAGE */
.page { padding: 32px 40px 80px; max-width:1500px; margin:0 auto; }
.sec-label { font-size:10.5px; font-weight:650; letter-spacing:0.09em; text-transform:uppercase; color:var(--text-tertiary); margin-bottom:16px; }

/* MARKET TICKER */
.ticker-wrap { overflow-x:auto; padding-bottom:4px; margin-bottom:32px; }
.ticker-row { display:flex; gap:10px; min-width:max-content; }
.ticker-card {
    background:var(--bg-card); border:1px solid var(--border);
    border-radius:12px; padding:14px 18px; cursor:pointer;
    transition:all 0.18s; min-width:140px; flex-shrink:0;
}
.ticker-card:hover { border-color:var(--border-bright); background:var(--bg-card2); transform:translateY(-1px); }
.ticker-card.active { border-color:rgba(10,132,255,0.5)!important; background:rgba(10,132,255,0.07)!important; }
.ticker-coin { display:flex; align-items:center; gap:7px; margin-bottom:8px; }
.ticker-icon { width:22px; height:22px; border-radius:6px; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:700; }
.ticker-sym { font-size:12px; font-weight:650; color:var(--text-primary); letter-spacing:0.02em; }
.ticker-price { font-size:14px; font-weight:600; color:var(--text-primary); font-family:var(--mono)!important; letter-spacing:-0.3px; margin-bottom:3px; }
.ticker-chg { font-size:11px; font-weight:500; }
.chg-up { color:var(--accent-green); }
.chg-dn { color:var(--accent-red); }
.chg-flat { color:var(--text-tertiary); }
.ticker-sig { display:inline-block; font-size:9.5px; font-weight:700; letter-spacing:0.06em; padding:2px 7px; border-radius:5px; margin-top:6px; }
.sig-buy  { background:var(--accent-green-dim); color:var(--accent-green); border:1px solid rgba(48,209,88,0.25); }
.sig-sell { background:var(--accent-red-dim);   color:var(--accent-red);   border:1px solid rgba(255,69,58,0.22); }
.sig-hold { background:var(--accent-amber-dim); color:var(--accent-amber); border:1px solid rgba(255,214,10,0.2); }

/* SIGNAL HERO */
.signal-hero {
    background:var(--bg-card); border:1px solid var(--border);
    border-radius:20px; padding:34px 36px; position:relative; overflow:hidden; margin-bottom:14px;
}
.signal-hero::before { content:''; position:absolute; top:0;left:0;right:0; height:1px; }
.hero-buy::before  { background:linear-gradient(90deg,transparent,rgba(48,209,88,0.5),transparent); }
.hero-sell::before { background:linear-gradient(90deg,transparent,rgba(255,69,58,0.5),transparent); }
.hero-hold::before { background:linear-gradient(90deg,transparent,rgba(255,214,10,0.4),transparent); }

.hero-top { display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:24px; }
.hero-coin-info { display:flex; align-items:center; gap:14px; }
.hero-coin-icon { width:48px; height:48px; border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:800; }
.hero-coin-name { font-size:22px; font-weight:700; letter-spacing:-0.5px; }
.hero-coin-pair { font-size:12px; color:var(--text-secondary); font-family:var(--mono)!important; margin-top:2px; }
.hero-right { display:flex; flex-direction:column; align-items:flex-end; gap:8px; }

.sig-badge { display:inline-flex; align-items:center; gap:8px; padding:10px 22px; border-radius:12px; font-size:20px; font-weight:750; letter-spacing:-0.2px; }
.badge-buy  { background:var(--accent-green-dim); color:var(--accent-green); border:1px solid rgba(48,209,88,0.3); }
.badge-sell { background:var(--accent-red-dim);   color:var(--accent-red);   border:1px solid rgba(255,69,58,0.28); }
.badge-hold { background:var(--accent-amber-dim); color:var(--accent-amber); border:1px solid rgba(255,214,10,0.25); }

.conf-tag { display:inline-flex; align-items:center; gap:5px; padding:5px 12px; border-radius:18px; font-size:11px; font-weight:650; }
.conf-high   { background:rgba(10,132,255,0.12); color:var(--accent-blue); border:1px solid rgba(10,132,255,0.22); }
.conf-medium { background:var(--accent-amber-dim); color:var(--accent-amber); border:1px solid rgba(255,214,10,0.2); }
.conf-low    { background:rgba(255,255,255,0.05); color:var(--text-secondary); border:1px solid var(--border); }

.hero-price { font-size:44px; font-weight:300; letter-spacing:-2px; font-variant-numeric:tabular-nums; margin-bottom:4px; }
.hero-meta  { font-size:11.5px; color:var(--text-secondary); font-family:var(--mono)!important; }
.hero-reason { background:rgba(255,255,255,0.025); border:1px solid var(--border); border-radius:11px; padding:14px 18px; margin-top:22px; font-size:13.5px; line-height:1.65; color:rgba(255,255,255,0.68); }
.hero-reason b { color:var(--text-primary); font-weight:550; }

/* INDICATOR PILLS */
.ind-row { display:flex; gap:8px; flex-wrap:wrap; margin-top:18px; }
.ind-pill { display:flex; align-items:center; gap:7px; padding:7px 13px; background:rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:8px; font-size:11.5px; font-family:var(--mono)!important; }
.ind-pill .il { color:var(--text-tertiary); }
.ind-pill .iv { color:var(--text-primary); font-weight:600; }
.ind-bull { border-color:rgba(48,209,88,0.2)!important; background:rgba(48,209,88,0.04)!important; }
.ind-bear { border-color:rgba(255,69,58,0.2)!important; background:rgba(255,69,58,0.04)!important; }
.ind-neut { border-color:rgba(255,214,10,0.2)!important; background:rgba(255,214,10,0.04)!important; }

/* METRICS */
.metrics-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:11px; margin-bottom:14px; }
.metric-card { background:var(--bg-card); border:1px solid var(--border); border-radius:15px; padding:20px 22px; }
.metric-card:hover { border-color:var(--border-bright); }
.mlabel { font-size:10.5px; font-weight:600; letter-spacing:0.07em; text-transform:uppercase; color:var(--text-tertiary); margin-bottom:9px; }
.mval { font-size:26px; font-weight:650; letter-spacing:-0.4px; font-variant-numeric:tabular-nums; line-height:1; }
.msub { font-size:11px; color:var(--text-secondary); margin-top:5px; }
.mgreen { color:var(--accent-green)!important; }
.mred   { color:var(--accent-red)!important; }
.mblue  { color:var(--accent-blue)!important; }

/* MARKET OVERVIEW GRID */
.market-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:10px; margin-bottom:14px; }
.mkt-card { background:var(--bg-card); border:1px solid var(--border); border-radius:13px; padding:16px 18px; cursor:pointer; transition:all 0.16s; }
.mkt-card:hover { border-color:var(--border-bright); transform:translateY(-1px); }
.mkt-top { display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; }
.mkt-coin { display:flex; align-items:center; gap:8px; }
.mkt-icon { width:26px; height:26px; border-radius:7px; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; }
.mkt-sym { font-size:13px; font-weight:650; }
.mkt-price { font-size:16px; font-weight:600; font-family:var(--mono)!important; letter-spacing:-0.3px; margin-bottom:4px; }
.mkt-change { font-size:12px; font-weight:500; }

/* TABS */
.stTabs [data-baseweb="tab-list"] { background:transparent!important; border-bottom:1px solid var(--border)!important; gap:0!important; padding:0!important; margin-bottom:26px; }
.stTabs [data-baseweb="tab"] { background:transparent!important; color:var(--text-secondary)!important; font-family:var(--font)!important; font-size:13.5px!important; font-weight:500!important; padding:11px 20px!important; border:none!important; border-bottom:2px solid transparent!important; border-radius:0!important; transition:all 0.15s!important; }
.stTabs [aria-selected="true"] { color:var(--text-primary)!important; border-bottom:2px solid var(--accent-blue)!important; }
.stTabs [data-baseweb="tab-highlight"] { display:none!important; }
.stTabs [data-baseweb="tab-panel"] { padding:0!important; }

/* BUTTONS */
.stButton>button { background:var(--accent-blue)!important; color:white!important; border:none!important; border-radius:10px!important; font-family:var(--font)!important; font-size:13.5px!important; font-weight:550!important; padding:10px 22px!important; transition:all 0.15s!important; }
.stButton>button:hover { background:#0070E0!important; transform:translateY(-1px)!important; box-shadow:0 6px 20px rgba(10,132,255,0.28)!important; }

/* SELECT */
.stSelectbox>div>div { background:var(--bg-card)!important; border:1px solid var(--border)!important; color:var(--text-primary)!important; border-radius:10px!important; }

/* FILE UPLOADER */
.stFileUploader>div { background:rgba(255,255,255,0.02)!important; border:1px dashed rgba(255,255,255,0.1)!important; border-radius:12px!important; }

/* DATA TABLE */
.stDataFrame { background:transparent!important; }

/* DISCLAIMER */
.disclaimer { background:rgba(255,214,10,0.04); border:1px solid rgba(255,214,10,0.14); border-radius:9px; padding:11px 15px; font-size:11.5px; color:rgba(255,214,10,0.65); margin-top:12px; }

/* SCROLLBAR */
::-webkit-scrollbar { width:3px; height:3px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:rgba(255,255,255,0.08); border-radius:2px; }

/* BACKTEST CARD */
.bt-card { background:var(--bg-card); border:1px solid var(--border); border-radius:18px; padding:26px 30px; margin-bottom:14px; }
.bt-title { font-size:14px; font-weight:650; margin-bottom:3px; }
.bt-sub { font-size:11.5px; color:var(--text-secondary); margin-bottom:22px; }

.js-plotly-plot .plotly { background:transparent!important; }
</style>
""", unsafe_allow_html=True)

# ─── Signal Engine ────────────────────────────────────────────────────────────
def compute_rsi(series, period=14):
    delta = series.diff()
    gain  = delta.clip(lower=0).rolling(period).mean()
    loss  = (-delta.clip(upper=0)).rolling(period).mean()
    rs    = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))

def arima_trend(series):
    try:
        n = min(30, len(series))
        y = series.iloc[-n:].values
        x = np.arange(n)
        slope = np.polyfit(x, y, 1)[0]
        last  = y[-1]
        return last + slope, slope
    except Exception:
        return series.iloc[-1], 0.0

def generate_signal(df):
    df = df.copy().dropna()
    if len(df) < 55:
        return None
    close = df['close'].astype(float)
    ma20  = close.rolling(20).mean().iloc[-1]
    ma50  = close.rolling(50).mean().iloc[-1]
    rsi   = compute_rsi(close).iloc[-1]
    price = close.iloc[-1]
    prev  = close.iloc[-2]
    forecast, slope = arima_trend(close)
    arima_up  = slope > 0
    arima_pct = abs(slope / (price + 1e-9) * 100)

    bull, bull_r = 0, []
    bear, bear_r = 0, []

    if price > ma20:  bull += 1; bull_r.append(f"Price above MA20 (${ma20:,.2f})")
    if ma20  > ma50:  bull += 1; bull_r.append("MA20 > MA50 — Golden Cross")
    if 40 < rsi < 70: bull += 1; bull_r.append(f"RSI {rsi:.1f} — bullish momentum")
    if arima_up:      bull += 1; bull_r.append(f"ARIMA slope: +{arima_pct:.3f}% — uptrend")
    if price > prev:  bull += 0.5; bull_r.append("Last candle closed higher")

    if price < ma20:  bear += 1; bear_r.append(f"Price below MA20 (${ma20:,.2f})")
    if ma20  < ma50:  bear += 1; bear_r.append("MA20 < MA50 — Death Cross")
    if rsi   > 70:    bear += 1; bear_r.append(f"RSI {rsi:.1f} — overbought")
    elif rsi < 30:    bear += 1; bear_r.append(f"RSI {rsi:.1f} — oversold pressure")
    if not arima_up:  bear += 1; bear_r.append(f"ARIMA slope: -{arima_pct:.3f}% — downtrend")
    if price < prev:  bear += 0.5; bear_r.append("Last candle closed lower")

    diff = bull - bear
    if   diff >= 2.5:  sig="BUY";  conf="High" if diff>=3.5 else "Medium"; reasons=bull_r
    elif diff <= -2.5: sig="SELL"; conf="High" if diff<=-3.5 else "Medium"; reasons=bear_r
    elif abs(diff)<=1: sig="HOLD"; conf="Medium"; reasons=(bull_r[:1]+bear_r[:1]) or bull_r or bear_r
    else:              sig="BUY" if diff>0 else "SELL"; conf="Low"; reasons=bull_r if diff>0 else bear_r

    return {
        "signal": sig, "confidence": conf, "price": price,
        "ma20": ma20, "ma50": ma50, "rsi": rsi,
        "arima_up": arima_up, "arima_forecast": forecast, "arima_pct": arima_pct,
        "reason": ". ".join(reasons) + ".",
        "bull": bull, "bear": bear,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
    }

def run_backtest(df):
    df    = df.copy().dropna()
    close = df['close'].astype(float)
    ma20  = close.rolling(20).mean()
    ma50  = close.rolling(50).mean()
    rsi_s = compute_rsi(close)
    trades, in_t, ep = [], False, 0.0
    equity, peak, max_dd = 10000.0, 10000.0, 0.0
    for i in range(55, len(df)):
        p,r,m20,m50 = close.iloc[i], rsi_s.iloc[i], ma20.iloc[i], ma50.iloc[i]
        if (p>m20 and m20>m50 and 40<r<70) and not in_t: ep=p; in_t=True
        elif (p<m20 and m20<m50 and (r>65 or r<35)) and in_t:
            pnl = (p-ep)/ep*100; equity *= (1+pnl/100)
            peak = max(peak,equity); max_dd = max(max_dd,(peak-equity)/peak*100)
            trades.append({"Entry":f"${ep:,.2f}","Exit":f"${p:,.2f}","P&L %":f"{pnl:+.2f}%","Result":"✅ Win" if pnl>0 else "❌ Loss"})
            in_t = False
    total = len(trades); wins = sum(1 for t in trades if "Win" in t["Result"])
    return {"total":total,"win_rate":(wins/total*100 if total else 0),"profit":(equity-10000)/100,"max_dd":max_dd,"equity":equity,"trades":trades[-10:]}

# ─── Data Fetchers ────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def fetch_binance(symbol="BTCUSDT", interval="15m", limit=200):
    try:
        url  = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        data = requests.get(url, timeout=10).json()
        if not isinstance(data, list): return None
        df = pd.DataFrame(data, columns=['ts','open','high','low','close','volume','ct','qav','n','tbbv','tbqv','ig'])
        df['datetime'] = pd.to_datetime(df['ts'], unit='ms')
        for c in ['open','high','low','close','volume']: df[c] = pd.to_numeric(df[c])
        return df[['datetime','open','high','low','close','volume']]
    except: return None

@st.cache_data(ttl=30)
def fetch_ticker(symbol):
    try:
        url  = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        data = requests.get(url, timeout=6).json()
        return {"price": float(data.get("lastPrice",0)), "change": float(data.get("priceChangePercent",0))}
    except: return {"price": 0, "change": 0}

def parse_csv(file):
    try:
        df = pd.read_csv(file)
        df.columns = [c.strip().lower() for c in df.columns]
        if 'datetime' not in df.columns and 'date' in df.columns: df.rename(columns={'date':'datetime'},inplace=True)
        df['datetime'] = pd.to_datetime(df['datetime'])
        for c in ['open','high','low','close','volume']:
            if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce')
        return df.sort_values('datetime').reset_index(drop=True)
    except: return None

# ─── Chart ────────────────────────────────────────────────────────────────────
def build_chart(df):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.72,0.28], vertical_spacing=0.02)
    fig.add_trace(go.Candlestick(
        x=df['datetime'], open=df['open'], high=df['high'], low=df['low'], close=df['close'],
        increasing_line_color='#30D158', decreasing_line_color='#FF453A',
        increasing_fillcolor='rgba(48,209,88,0.75)', decreasing_fillcolor='rgba(255,69,58,0.75)',
        line_width=1, name='Price'), row=1, col=1)
    cl  = df['close'].astype(float)
    ma20= cl.rolling(20).mean(); ma50= cl.rolling(50).mean()
    fig.add_trace(go.Scatter(x=df['datetime'],y=ma20,name='MA20',line=dict(color='rgba(10,132,255,0.85)',width=1.5)),row=1,col=1)
    fig.add_trace(go.Scatter(x=df['datetime'],y=ma50,name='MA50',line=dict(color='rgba(255,214,10,0.75)',width=1.5,dash='dot')),row=1,col=1)
    rsi = compute_rsi(cl)
    fig.add_trace(go.Scatter(x=df['datetime'],y=rsi,name='RSI',line=dict(color='rgba(10,132,255,0.6)',width=1.5),fill='tozeroy',fillcolor='rgba(10,132,255,0.05)'),row=2,col=1)
    for lvl,col in [(70,'rgba(255,69,58,0.3)'),(30,'rgba(48,209,88,0.3)'),(50,'rgba(255,255,255,0.08)')]:
        fig.add_hline(y=lvl,line_dash="dot",line_color=col,row=2,col=1)
    axis_style = dict(showgrid=True,gridcolor='rgba(255,255,255,0.04)',zeroline=False,tickfont=dict(color='rgba(255,255,255,0.28)',size=10))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0,r=0,t=0,b=0), height=460,
        showlegend=True,
        legend=dict(bgcolor='rgba(15,15,15,0.8)',bordercolor='rgba(255,255,255,0.07)',borderwidth=1,
                    font=dict(color='rgba(255,255,255,0.45)',size=10),x=0,y=1),
        xaxis=dict(**axis_style,rangeslider=dict(visible=False),showspikes=True,spikecolor='rgba(255,255,255,0.12)',spikethickness=1),
        yaxis=dict(**axis_style,side='right',tickprefix='$',tickformat=',.2f'),
        xaxis2=dict(**axis_style), yaxis2=dict(**axis_style,side='right',range=[0,100]),
        hovermode='x unified',
        hoverlabel=dict(bgcolor='rgba(15,15,15,0.95)',bordercolor='rgba(255,255,255,0.08)',font=dict(color='white',size=11.5)),
    )
    return fig

# ─── UI Helpers ──────────────────────────────────────────────────────────────
def fmt_price(price):
    if price >= 1000:  return f"${price:,.2f}"
    if price >= 1:     return f"${price:.4f}"
    return f"${price:.6f}"

def render_signal_hero(sig, coin_key):
    meta  = COINS[coin_key]
    s     = sig['signal']
    c     = sig['confidence']
    scls  = s.lower(); ccls = c.lower()
    icon  = "↑" if s=="BUY" else "↓" if s=="SELL" else "→"
    cicon = "⬤" if c=="High" else "◉" if c=="Medium" else "○"
    color = meta['color']
    st.markdown(f"""
    <div class="signal-hero hero-{scls}">
      <div class="hero-top">
        <div class="hero-coin-info">
          <div class="hero-coin-icon" style="background:{color}22;border:1px solid {color}44;">
            <span style="color:{color}">{meta['icon']}</span>
          </div>
          <div>
            <div class="hero-coin-name">{meta['name']}</div>
            <div class="hero-coin-pair">{meta['symbol']} · 15m · {sig['timestamp']}</div>
          </div>
        </div>
        <div class="hero-right">
          <div class="sig-badge badge-{scls}">{icon} {s}</div>
          <div class="conf-tag conf-{ccls}">{cicon}&nbsp; {c} Confidence</div>
        </div>
      </div>
      <div class="hero-price">{fmt_price(sig['price'])}</div>
      <div class="hero-reason"><b>Analysis:</b> {sig['reason']}</div>
      <div class="ind-row">
        <div class="ind-pill {'ind-bull' if sig['price']>sig['ma20'] else 'ind-bear'}">
          <span class="il">MA20</span><span class="iv">{fmt_price(sig['ma20'])}</span>
        </div>
        <div class="ind-pill {'ind-bull' if sig['ma20']>sig['ma50'] else 'ind-bear'}">
          <span class="il">MA50</span><span class="iv">{fmt_price(sig['ma50'])}</span>
        </div>
        <div class="ind-pill {'ind-bull' if 40<sig['rsi']<70 else ('ind-bear' if sig['rsi']>70 or sig['rsi']<30 else 'ind-neut')}">
          <span class="il">RSI</span><span class="iv">{sig['rsi']:.1f}</span>
        </div>
        <div class="ind-pill {'ind-bull' if sig['arima_up'] else 'ind-bear'}">
          <span class="il">ARIMA</span><span class="iv">{'▲' if sig['arima_up'] else '▼'} {fmt_price(sig['arima_forecast'])}</span>
        </div>
        <div class="ind-pill">
          <span class="il">Bull Score</span><span class="iv" style="color:var(--accent-green)">{sig['bull']:.1f}</span>
        </div>
        <div class="ind-pill">
          <span class="il">Bear Score</span><span class="iv" style="color:var(--accent-red)">{sig['bear']:.1f}</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

def render_bt_metrics(bt):
    wr, pnl, dd = bt['win_rate'], bt['profit'], bt['max_dd']
    st.markdown(f"""
    <div class="metrics-grid">
      <div class="metric-card"><div class="mlabel">Total Trades</div><div class="mval mblue">{bt['total']}</div><div class="msub">Simulated entries</div></div>
      <div class="metric-card"><div class="mlabel">Win Rate</div><div class="mval {'mgreen' if wr>=55 else 'mred'}">{wr:.1f}%</div><div class="msub">Profitable trades</div></div>
      <div class="metric-card"><div class="mlabel">Net Profit</div><div class="mval {'mgreen' if pnl>=0 else 'mred'}">{pnl:+.2f}%</div><div class="msub">From $10,000 base</div></div>
      <div class="metric-card"><div class="mlabel">Max Drawdown</div><div class="mval mred">-{dd:.2f}%</div><div class="msub">Peak-to-trough</div></div>
    </div>
    """, unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
if 'selected_coin' not in st.session_state:
    st.session_state.selected_coin = 'BTC'

# ─── NAV ─────────────────────────────────────────────────────────────────────
now_str = datetime.now().strftime("%d %b %Y · %H:%M:%S")
st.markdown(f"""
<div class="cipher-nav">
  <div class="cipher-logo">
    <div class="cipher-logo-icon">⚡</div>
    Cipher
  </div>
  <div class="nav-right">
    <div class="nav-time">{now_str} UTC</div>
    <div class="live-pill"><div class="live-dot"></div>Live · Binance</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── PAGE ────────────────────────────────────────────────────────────────────
st.markdown('<div class="page">', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["⚡  Live Signals", "🌐  Market Overview", "📂  CSV Analysis", "📊  Backtest"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — LIVE SIGNALS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-label">Select Coin</div>', unsafe_allow_html=True)

    # ── Ticker strip (top 12 coins) ──
    top12 = list(COINS.keys())[:12]
    ticker_html = '<div class="ticker-wrap"><div class="ticker-row">'
    ticker_data  = {}
    for ck in top12:
        td = fetch_ticker(COINS[ck]['symbol'])
        ticker_data[ck] = td
        chg_cls = "chg-up" if td['change']>=0 else "chg-dn"
        chg_sym = "+" if td['change']>=0 else ""
        price_str = fmt_price(td['price']) if td['price'] else "—"

        # quick signal for badge
        df_q = fetch_binance(COINS[ck]['symbol'], "15m", 70)
        sig_q = generate_signal(df_q) if df_q is not None and len(df_q)>=55 else None
        sig_label = sig_q['signal'] if sig_q else "—"
        active_cls = "active" if ck == st.session_state.selected_coin else ""
        color = COINS[ck]['color']
        ticker_html += f"""
        <div class="ticker-card {active_cls}" onclick="void(0)">
          <div class="ticker-coin">
            <div class="ticker-icon" style="background:{color}22;color:{color}">{COINS[ck]['icon']}</div>
            <span class="ticker-sym">{ck}</span>
          </div>
          <div class="ticker-price">{price_str}</div>
          <div class="ticker-chg {chg_cls}">{chg_sym}{td['change']:.2f}%</div>
          <div class="ticker-sig sig-{sig_label.lower()}">{sig_label}</div>
        </div>"""
    ticker_html += '</div></div>'
    st.markdown(ticker_html, unsafe_allow_html=True)

    # ── Coin selector ──
    coin_options = [f"{v['icon']} {k} — {v['name']}" for k,v in COINS.items()]
    coin_keys    = list(COINS.keys())
    default_idx  = coin_keys.index(st.session_state.selected_coin)
    selected_opt = st.selectbox("", coin_options, index=default_idx, label_visibility="collapsed")
    selected_key = coin_keys[coin_options.index(selected_opt)]
    st.session_state.selected_coin = selected_key
    coin_meta = COINS[selected_key]

    # ── Fetch & signal ──
    with st.spinner(f"AI analyzing {selected_key}..."):
        df_live = fetch_binance(coin_meta['symbol'], "15m", 200)

    if df_live is None or len(df_live) < 60:
        st.markdown("""
        <div style="text-align:center;padding:60px 0">
          <div style="font-size:30px;margin-bottom:14px">🌐</div>
          <div style="font-size:15px;font-weight:550;margin-bottom:6px">Connection Error</div>
          <div style="font-size:12.5px;color:rgba(255,255,255,0.35)">
            Unable to reach Binance API. Try the CSV tab.
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        sig = generate_signal(df_live)
        if sig:
            st.markdown('<div class="sec-label" style="margin-top:24px">Current Signal</div>', unsafe_allow_html=True)
            render_signal_hero(sig, selected_key)
            st.markdown('<div class="sec-label" style="margin-top:28px">Price Chart · 15m</div>', unsafe_allow_html=True)
            st.plotly_chart(build_chart(df_live), use_container_width=True,
                config={'displayModeBar':True,'displaylogo':False,'modeBarButtonsToRemove':['lasso2d','select2d','autoScale2d']})
            st.markdown('<div class="disclaimer">⚠️ Educational only. Not financial advice. Past performance ≠ future results.</div>', unsafe_allow_html=True)

    st.markdown('<script>setTimeout(()=>window.location.reload(),60000)</script>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MARKET OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-label">All Coins — Live Signals</div>', unsafe_allow_html=True)
    with st.spinner("Fetching signals for all coins..."):
        all_signals = {}
        for ck, cm in COINS.items():
            df_tmp = fetch_binance(cm['symbol'], "15m", 80)
            sig_tmp = generate_signal(df_tmp) if df_tmp is not None and len(df_tmp)>=55 else None
            td_tmp  = fetch_ticker(cm['symbol'])
            all_signals[ck] = {"sig": sig_tmp, "td": td_tmp}

    # Summary counts
    buys  = sum(1 for v in all_signals.values() if v['sig'] and v['sig']['signal']=="BUY")
    sells = sum(1 for v in all_signals.values() if v['sig'] and v['sig']['signal']=="SELL")
    holds = sum(1 for v in all_signals.values() if v['sig'] and v['sig']['signal']=="HOLD")
    st.markdown(f"""
    <div class="metrics-grid" style="margin-bottom:24px">
      <div class="metric-card"><div class="mlabel">Total Coins</div><div class="mval mblue">{len(COINS)}</div><div class="msub">Tracked live</div></div>
      <div class="metric-card"><div class="mlabel">BUY Signals</div><div class="mval mgreen">{buys}</div><div class="msub">Bullish coins</div></div>
      <div class="metric-card"><div class="mlabel">SELL Signals</div><div class="mval mred">{sells}</div><div class="msub">Bearish coins</div></div>
      <div class="metric-card"><div class="mlabel">HOLD Signals</div><div class="mval" style="color:var(--accent-amber)">{holds}</div><div class="msub">Neutral coins</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Grid
    grid_html = '<div class="market-grid">'
    for ck, data in all_signals.items():
        cm   = COINS[ck]
        sig  = data['sig']
        td   = data['td']
        s    = sig['signal'] if sig else "—"
        chg  = td['change']
        chg_cls = "chg-up" if chg>=0 else "chg-dn"
        chg_sym = "+" if chg>=0 else ""
        price_str = fmt_price(td['price']) if td['price'] else "—"
        color = cm['color']
        conf  = sig['confidence'] if sig else ""
        rsi_v = f"{sig['rsi']:.0f}" if sig else "—"
        grid_html += f"""
        <div class="mkt-card">
          <div class="mkt-top">
            <div class="mkt-coin">
              <div class="mkt-icon" style="background:{color}22;color:{color}">{cm['icon']}</div>
              <span class="mkt-sym">{ck}</span>
            </div>
            <div class="ticker-sig sig-{s.lower()}">{s}</div>
          </div>
          <div class="mkt-price">{price_str}</div>
          <div class="mkt-change {chg_cls}">{chg_sym}{chg:.2f}% (24h)</div>
          <div style="margin-top:8px;display:flex;gap:6px;flex-wrap:wrap">
            <div class="ind-pill" style="padding:4px 8px">
              <span class="il" style="font-size:10px">RSI</span>
              <span class="iv" style="font-size:10px">{rsi_v}</span>
            </div>
            <div class="ind-pill" style="padding:4px 8px">
              <span class="il" style="font-size:10px">CONF</span>
              <span class="iv" style="font-size:10px">{conf}</span>
            </div>
          </div>
        </div>"""
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

    # Table
    st.markdown('<div class="sec-label" style="margin-top:28px">Signal Table</div>', unsafe_allow_html=True)
    rows = []
    for ck, data in all_signals.items():
        sig = data['sig']; td = data['td']; cm = COINS[ck]
        rows.append({
            "Coin":       f"{cm['icon']} {ck}",
            "Name":       cm['name'],
            "Price":      fmt_price(td['price']) if td['price'] else "—",
            "24h Change": f"{'+' if td['change']>=0 else ''}{td['change']:.2f}%",
            "Signal":     sig['signal'] if sig else "—",
            "Confidence": sig['confidence'] if sig else "—",
            "RSI":        f"{sig['rsi']:.1f}" if sig else "—",
            "MA Cross":   ("🟢 Golden" if sig['ma20']>sig['ma50'] else "🔴 Death") if sig else "—",
            "ARIMA":      ("▲ Up" if sig['arima_up'] else "▼ Down") if sig else "—",
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.markdown('<div class="disclaimer">⚠️ Educational only. Not financial advice.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CSV ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-label">Upload OHLCV Data</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("CSV format: datetime, open, high, low, close, volume", type=["csv"])

    if uploaded:
        with st.spinner("Parsing and analyzing..."):
            df_csv = parse_csv(uploaded)
        if df_csv is None or len(df_csv) < 60:
            st.error("Could not parse CSV. Required columns: datetime, open, high, low, close, volume")
        else:
            sig_csv = generate_signal(df_csv)
            if sig_csv:
                sig_csv['timestamp'] = f"{df_csv['datetime'].iloc[-1].strftime('%Y-%m-%d %H:%M')} (CSV)"
                csv_key = st.selectbox("Coin tag for display:", list(COINS.keys()), index=0)
                render_signal_hero(sig_csv, csv_key)
                st.markdown('<div class="sec-label" style="margin-top:28px">Chart</div>', unsafe_allow_html=True)
                st.plotly_chart(build_chart(df_csv), use_container_width=True,
                    config={'displayModeBar':True,'displaylogo':False,'modeBarButtonsToRemove':['lasso2d','select2d']})
                st.markdown('<div class="disclaimer">⚠️ Educational only. Not financial advice.</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="padding:32px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);
             border-radius:14px;text-align:center;margin-top:8px">
          <div style="font-size:28px;margin-bottom:10px">📊</div>
          <div style="font-size:14px;font-weight:500;margin-bottom:6px">No file uploaded</div>
          <div style="font-size:12px;color:rgba(255,255,255,0.3)">Upload a CSV or download the sample below</div>
        </div>""", unsafe_allow_html=True)
        sample = pd.DataFrame({
            'datetime': pd.date_range("2024-01-01", periods=100, freq="15min").strftime("%Y-%m-%d %H:%M:%S"),
            'open':  [42000 + np.random.randn()*300 for _ in range(100)],
            'high':  [42200 + np.random.randn()*300 for _ in range(100)],
            'low':   [41800 + np.random.randn()*300 for _ in range(100)],
            'close': [42100 + np.random.randn()*300 for _ in range(100)],
            'volume':[np.random.randint(200,800) for _ in range(100)],
        })
        st.download_button("⬇  Download Sample CSV", sample.to_csv(index=False), "cipher_sample.csv", "text/csv")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — BACKTEST
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-label">Strategy Backtest</div>', unsafe_allow_html=True)
    st.markdown('<div class="bt-card"><div class="bt-title">Simulation Settings</div><div class="bt-sub">Entry on BUY (MA crossover + RSI) · Exit on SELL · $10,000 starting equity · No fees modeled</div></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        bt_coin = st.selectbox("Coin", [f"{v['icon']} {k} — {v['name']}" for k,v in COINS.items()], key="bt_coin")
        bt_key  = list(COINS.keys())[[f"{v['icon']} {k} — {v['name']}" for k,v in COINS.items()].index(bt_coin)]
    with col2:
        bt_tf = st.selectbox("Timeframe", ["15m","1h","4h","1d"], key="bt_tf")
    with col3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_bt = st.button("Run Backtest →")

    if run_bt:
        with st.spinner(f"Running backtest on {bt_key} {bt_tf}..."):
            df_bt = fetch_binance(COINS[bt_key]['symbol'], bt_tf, 500)
        if df_bt is None or len(df_bt) < 60:
            st.error("Could not fetch enough data.")
        else:
            bt = run_backtest(df_bt)
            st.markdown('<div class="sec-label" style="margin-top:8px">Performance</div>', unsafe_allow_html=True)
            render_bt_metrics(bt)

            if bt['trades']:
                st.markdown('<div class="sec-label" style="margin-top:24px">Last 10 Trades</div>', unsafe_allow_html=True)
                st.dataframe(pd.DataFrame(bt['trades']), use_container_width=True, hide_index=True)

            # Equity curve
            cl   = df_bt['close'].astype(float)
            ma20 = cl.rolling(20).mean(); ma50 = cl.rolling(50).mean(); rsi_s = compute_rsi(cl)
            eq_vals = [10000.0]; ts_vals = [df_bt['datetime'].iloc[55]]
            in_t, ep = False, 0.0; cur_eq = 10000.0
            for i in range(55, len(df_bt)):
                p,r,m20,m50 = cl.iloc[i], rsi_s.iloc[i], ma20.iloc[i], ma50.iloc[i]
                if (p>m20 and m20>m50 and 40<r<70) and not in_t: ep=p; in_t=True
                elif (p<m20 and m20<m50 and (r>65 or r<35)) and in_t:
                    cur_eq *= (1+(p-ep)/ep); in_t=False
                eq_vals.append(cur_eq); ts_vals.append(df_bt['datetime'].iloc[i])

            fig_eq = go.Figure()
            fig_eq.add_trace(go.Scatter(x=ts_vals, y=eq_vals, name='Equity',
                line=dict(color='#0A84FF',width=2), fill='tozeroy', fillcolor='rgba(10,132,255,0.06)'))
            fig_eq.add_hline(y=10000, line_dash="dot", line_color="rgba(255,255,255,0.1)")
            fig_eq.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=200, margin=dict(l=0,r=0,t=6,b=0), showlegend=False,
                xaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,0.04)',zeroline=False,
                           tickfont=dict(color='rgba(255,255,255,0.28)',size=10)),
                yaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,0.04)',zeroline=False,
                           side='right',tickprefix='$',tickformat=',.0f',
                           tickfont=dict(color='rgba(255,255,255,0.28)',size=10)),
                hovermode='x unified',
                hoverlabel=dict(bgcolor='rgba(15,15,15,0.95)',font=dict(color='white',size=11)),
            )
            st.markdown('<div class="sec-label" style="margin-top:24px">Equity Curve</div>', unsafe_allow_html=True)
            st.plotly_chart(fig_eq, use_container_width=True, config={'displaylogo':False})
            st.markdown('<div class="disclaimer">⚠️ Backtesting is simulation only. Slippage and fees not modeled. Not financial advice.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
