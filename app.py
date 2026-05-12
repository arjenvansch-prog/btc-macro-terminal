import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta
import random
@st.cache_data(ttl=60)
def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    price = data["bitcoin"]["usd"]
    change = data["bitcoin"]["usd_24h_change"]

    return price, change
def get_fear_greed():
    url = "https://api.alternative.me/fng/"
    response = requests.get(url)
    data = response.json()

    value = int(data["data"][0]["value"])
    label = data["data"][0]["value_classification"]

    return value, label
st.set_page_config(page_title="BTC Macro Terminal", layout="wide")
@st.cache_data(ttl=300)
def get_btc_candles(period="7d", interval="1h"):
    data = yf.download(
        "BTC-EUR",
        period=period,
        interval=interval,
        progress=False,
        threads=False
    )

    if data.empty:
        return None

    return data
st.title("Bitcoin Macro Terminal")
btc_price, btc_change = get_bitcoin_price()
fear_value, fear_label = get_fear_greed()
if btc_change > 0 and fear_value > 50:
    regime = "🟢 Risk-On"
elif btc_change < 0 and fear_value < 50:
    regime = "🔴 Risk-Off"
else:
    regime = "🟡 Neutral"
    st.subheader(f"Market Regime: {regime}")
metrics = {
    "Bitcoin Price": (btc_price, btc_change),
    "Fed Outlook": (3.95, -0.2),
}
@st.cache_data(ttl=300)
def get_btc_history():
    data = yf.download(
        "BTC-USD",
        period="1y",
        interval="1d",
        progress=False,
        threads=False
    )

    data.reset_index(inplace=True)

    return data
btc_history = get_btc_candles()
timeframe = st.radio(
    "📅 Kies periode:",
    ["1U", "1D", "1W", "1M", "1Y", "ALL"],
    horizontal=True
)

if timeframe == "1U":
    filtered_data = btc_history.tail(24)

elif timeframe == "1D":
    filtered_data = btc_history.tail(24)

elif timeframe == "1W":
    filtered_data = btc_history.tail(7)

elif timeframe == "1M":
    filtered_data = btc_history.tail(30)

elif timeframe == "1Y":
    filtered_data = btc_history.tail(365)

else:
    filtered_data = btc_history
@st.cache_data(ttl=300)
def get_fear_greed():
    url = "https://api.alternative.me/fng/"
    response = requests.get(url)
    data = response.json()

    value = int(data["data"][0]["value"])
    label = data["data"][0]["value_classification"]

    return value, label
if isinstance(btc_history.columns, pd.MultiIndex):
    btc_history.columns = btc_history.columns.droplevel(1)
btc_history.columns = btc_history.columns.get_level_values(0)
btc_history = btc_history.reset_index()

fig = go.Figure(data=[go.Candlestick(
    x=btc_history["Date"],
    open=btc_history["Open"],
    high=btc_history["High"],
    low=btc_history["Low"],
    close=btc_history["Close"]
)])

fig.update_layout(
    title="Bitcoin Candlestick Chart",
    xaxis_title="Date",
    yaxis_title="Price"
)

st.plotly_chart(fig, use_container_width=True)
fear_value, fear_classification = get_fear_greed()
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=fear_value,
))
st.divider()

st.subheader("🏦 Institutionele Bitcoin-markt")

st.info(
    "Vanaf 29 mei 2026 verandert de Bitcoin-marktstructuur: "
    "CME gaat crypto futures en opties 24/7 verhandelen. "
    "Daardoor worden oude CME weekend-gaps minder belangrijk."
)

st.write("""
Bitcoin wordt steeds meer een institutionele macro-asset.

Let daarom niet alleen op prijs, maar ook op:
- volatiliteit
- volume
- trend boven/onder gemiddelde
- macro en liquiditeit
- derivatenmarkt
"""),
gauge = {
        "axis": {"range": [0, 100]},
        "bar": {"thickness": 0.3},
"steps": [
    {"range": [0, 25], "color": "red"},
    {"range": [25, 50], "color": "orange"},
    {"range": [50, 75], "color": "yellow"},
    {"range": [75, 100], "color": "green"}
                ]
        } 
        
st.plotly_chart(fig_gauge, use_container_width=True)
cols = st.columns(3)
items = list(metrics.items())
for i, (name, values) in enumerate(items):
    value, delta = values
    with cols[i % 3]:
        st.metric(name, value, f"{delta}%")

macro_score = 68

st.subheader("Macro Phase")

if macro_score >= 70:
    st.success("Bullish Expansion")
elif macro_score >= 40:
    st.warning("Accumulation Phase")
else:
    st.error("Bearish Risk")

dates = []
scores = []

current = 55

for i in range(90):
    dates.append(datetime.today() - timedelta(days=89-i))
    current += random.uniform(-2, 2)
    current = max(20, min(90, current))
    scores.append(current)

df = pd.DataFrame({
    "Date": dates,
    "MacroScore": scores
})

fig = px.bar(df, x="Date", y="MacroScore", title="Historical Macro Trend")

st.plotly_chart(fig, use_container_width=True)

st.subheader("Whale Intelligence")

whales = pd.DataFrame({
    "Signal": [
        "Exchange Outflows",
        "Cold Storage Growth",
        "Large Wallet Accumulation",
        "Miner Selling Pressure"
    ],
    "Status": [
        "Bullish",
        "Bullish",
        "Bullish",
        "Neutral"
    ]
})

st.dataframe(whales, use_container_width=True)

st.subheader("AI Recommendation")

st.info("Prototype V1 ready for live API integrations.")
