import streamlit as st
import requests
import asyncio
import websockets
import json
import threading
import time

API_URL = "http://127.0.0.1:8000"
WS_URL = "ws://127.0.0.1:8000/ws/tape"

st.set_page_config(page_title="AI Trading System", layout="wide")
st.title("AI Trading System — Real‑Time Dashboard")

# ---------------------------
# GLOBAL SHARED DATA (thread-safe)
# ---------------------------

tape_events = []   # <--- NOT session_state


# ---------------------------
# WEBSOCKET LISTENER (background thread)
# ---------------------------

async def websocket_listener():
    global tape_events
    async with websockets.connect(WS_URL) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)

            tape_events.append(data)
            if len(tape_events) > 50:
                tape_events = tape_events[-50:]


def start_ws_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_listener())


# Start WebSocket listener ONCE
if "ws_thread_started" not in st.session_state:
    threading.Thread(target=start_ws_thread, daemon=True).start()
    st.session_state.ws_thread_started = True


# ---------------------------
# LAYOUT
# ---------------------------

col1, col2 = st.columns(2)

# LEFT SIDE = TAPE STREAM
tape_stream_box = col1.container()
latest_tape_box = col1.container()

# RIGHT SIDE = SIGNALS
signals_latest_box = col2.container()
signals_all_box = col2.container()
signals_filter_box = col2.container()


# ---------------------------
# SIGNALS SECTION (your original code)
# ---------------------------

with signals_latest_box:
    st.header("Latest Signal")
    latest = requests.get(f"{API_URL}/signals/latest").json()
    st.json(latest)

with signals_all_box:
    st.header("All Signals")
    all_signals = requests.get(f"{API_URL}/signals").json()
    st.json(all_signals)

with signals_filter_box:
    st.header("Filter Signals")
    signal_type = st.text_input("Enter signal type (e.g., Liquidity Sweep)")
    if st.button("Filter"):
        filtered = requests.get(
            f"{API_URL}/signals/filter",
            params={"signal_type": signal_type}
        ).json()
        st.json(filtered)


# ---------------------------
# REAL‑TIME TAPE STREAM
# ---------------------------

tape_stream_box.header("Real‑Time Tape Stream")
tape_stream_box.dataframe(tape_events, width="stretch")

latest_tape_box.header("Latest Tape Event")
if tape_events:
    latest_tape_box.json(tape_events[-1])
else:
    latest_tape_box.write("Waiting for tape events...")


# ---------------------------
# AUTO‑REFRESH EVERY 1 SECOND
# ---------------------------

time.sleep(1)
st.rerun()
