
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="BTC Macro Terminal", layout="wide")

st.title("Bitcoin Macro Terminal")

metrics = {
    "Bitcoin Price": (84250, 1.8),
    "ETF Inflow": (1850, 12.4),
    "Whale Score": (72, 6.2),
    "DXY": (99.4, -0.8),
    "Fear & Greed": (46, 3.0),
    "Fed Outlook": (3.95, -0.2),
}

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
