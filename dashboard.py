import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("AI Trading System - Signal Dashboard")

# Latest signal
st.header("Latest Signal")
latest = requests.get(f"{API_URL}/signals/latest").json()
st.json(latest)

# All signals
st.header("All Signals")
all_signals = requests.get(f"{API_URL}/signals").json()
st.json(all_signals)

# Filter signals
st.header("Filter Signals")
signal_type = st.text_input("Enter signal type (e.g., Liquididty Sweep)")
if st.button("Filter"):
    filtered = requests.get(f"{API_URL}/signals/filter", params={"signal_type": signal_type}).json()
    st.json(filtered)
    