from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pathlib import Path
import json
from datetime import datetime

# Import updated models
from signals.signal_model import Signal
from tape_reader.tape_model import TapeEvent
from diary.diary_model import DiaryEntry
from diary.diary_storage import load_entries, save_entries

app = FastAPI()

STORAGE_PATH = Path("signals/signal_storage.json")
TAPE_PATH = Path("tape_reader/tape_storage.json")

# ============================================================
# ROOT + HEALTH
# ============================================================

@app.get("/")
def root():
    return {"status": "AI Trading Brain Online"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "components": {
            "api": "online"
        }
    }

# ============================================================
# DIARY ENDPOINTS
# ============================================================

@app.post("/diary")
def create_diary_entry(entry: DiaryEntry):
    entries = load_entries()
    entries.append(entry.model_dump())
    save_entries(entries)
    return {"message": "Diary entry saved!"}


@app.get("/diary")
def get_diary_entries():
    return load_entries()

# ============================================================
# SIGNAL ENDPOINTS
# ============================================================

@app.post("/signals")
def create_signal(signal: Signal):
    try:
        if STORAGE_PATH.exists():
            raw = STORAGE_PATH.read_text().strip()
            data = json.loads(raw) if raw else []
        else:
            data = []
    except Exception:
        data = []
        STORAGE_PATH.write_text("[]")

    data.append(signal.model_dump(mode="json"))
    STORAGE_PATH.write_text(json.dumps(data, indent=4))

    return {"status": "ok", "stored": signal.model_dump(mode="json")}


@app.get("/signals")
def get_signals():
    raw = STORAGE_PATH.read_text().strip()
    data = json.loads(raw) if raw else []
    return data


@app.get("/signals/latest")
def get_latest_signal():
    raw = STORAGE_PATH.read_text().strip()
    if not raw:
        return {}
    
    data = json.loads(raw)
    if not data:
        return {}
    
    return data[-1]


@app.get("/signals/filter")
def filter_signals_(signal_type: str):
    raw = STORAGE_PATH.read_text().strip()
    data = json.loads(raw) if raw else []
    return [s for s in data if s.get("signal type") == signal_type]

# ============================================================
# TAPE LOGIC HELPERS
# ============================================================

def compute_delta(bid_volume: float, ask_volume: float) -> float:
    return ask_volume - bid_volume


def compute_imbalance(bid_volume: float, ask_volume: float) -> float:
    total = bid_volume + ask_volume
    if total == 0:
        return 0.0
    return (ask_volume - bid_volume) / total

# ============================================================
# WEBSOCKET TAPE STREAMING
# ============================================================

active_tape_connections: list[WebSocket] = []


@app.websocket("/ws/tape")
async def tape_websocket(websocket: WebSocket):
    await websocket.accept()
    active_tape_connections.append(websocket)

    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        if websocket in active_tape_connections:
            active_tape_connections.remove(websocket)

# ============================================================
# TAPE INGESTION + BROADCAST
# ============================================================

@app.post("/tape")
async def add_tape_event(event: TapeEvent):
    """
    Accepts a full microstructure tape event and enriches it with
    computed delta/imbalance if missing. Stores + broadcasts it.
    """

    enriched = event.model_dump(mode="json")

    # Compute delta if missing
    if enriched.get("delta") is None:
        enriched["delta"] = compute_delta(
            enriched["bid_volume"],
            enriched["ask_volume"]
        )

    # Compute imbalance if missing
    if enriched.get("imbalance") is None:
        enriched["imbalance"] = compute_imbalance(
            enriched["bid_volume"],
            enriched["ask_volume"]
        )

    # Store locally
    raw = TAPE_PATH.read_text().strip() if TAPE_PATH.exists() else "[]"
    data = json.loads(raw)
    data.append(enriched)
    TAPE_PATH.write_text(json.dumps(data, indent=2))

    # Broadcast to all WebSocket clients (MotiveWave)
    for conn in list(active_tape_connections):
        try:
            await conn.send_json(enriched)
        except Exception:
            if conn in active_tape_connections:
                active_tape_connections.remove(conn)

    return {"status": "ok", "stored": enriched}


@app.get("/tape")
def get_tape_events():
    if not TAPE_PATH.exists():
        return []
    raw = TAPE_PATH.read_text().strip()
    if not raw:
        return []
    return json.loads(raw)


@app.get("/tape/latest")
def get_latest_tape_event():
    if not TAPE_PATH.exists():
        return {}
    raw = TAPE_PATH.read_text().strip()
    if not raw:
        return {}
    data = json.loads(raw)
    if not data:
        return {}
    return data[-1]