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
st.set_page_config(page_title="BTC Macro Terminal", layout="wide")

st.title("Bitcoin Macro Terminal")
btc_price, btc_change = get_bitcoin_price()

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

@st.cache_data(ttl=300)
def get_fear_greed():
    url = "https://api.alternative.me/fng/"
    
    response = requests.get(url, timeout=10)
    data = response.json()

    value = int(data["data"][0]["value"])
    classification = data["data"][0]["value_classification"]

    return value, classification

if isinstance(btc_history.columns, pd.MultiIndex):
    btc_history.columns = btc_history.columns.get_level_values(0)
btc_history = btc_history.reset_index()

fig = px.line(
    btc_history,
    x="Date",
    y="Close",
    title="Bitcoin Price - Last 30 Days",
)

st.plotly_chart(fig, use_container_width=True)
fear_value, fear_classification = get_fear_greed()
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=fear_value,
    title={"text": f"Fear & Greed Index ({fear_label})"},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"thickness": 0.3},
        "steps": [
            {"range": [0, 25]},
            {"range": [25, 50]},
            {"range": [50, 75]},
            {"range": [75, 100]}
        ]
    }
))

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
