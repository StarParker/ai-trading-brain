from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import json

from signals.signal_model import Signal
from tape_reader.tape_model import TapeEvent
from diary.diary_model import DiaryEntry
from diary.diary_storage import load_entries, save_entries


app = FastAPI()

STORAGE_PATH = Path("signals/signal_storage.json")
TAPE_PATH = Path("tape_reader/tape_storage.json")


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


@app.post("/diary")
def create_diary_entry(entry: DiaryEntry):
    entries = load_entries()
    entries.append(entry.model_dump())
    save_entries(entries)
    return {"message": "Diary entry saved!"}


@app.get("/diary")
def get_diary_entries():
    return load_entries()


@app.post("/signals")
def create_signal(signal: Signal):
    try:
        if STORAGE_PATH.exists():
            raw = STORAGE_PATH.read_text().strip()
            data = json.loads(raw) if raw else []
        else:
            data = []
    except Exception:
        # Reset corrupted file
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
    return [s for s in data if s["signal type"] == signal_type]


TAPE_PATH = Path("tape_reader/tape_storage.json")


def compute_delta(bid_volume: int, ask_volume: int) -> int:
    return ask_volume - bid_volume


def compute_imbalance(bid_volume: int, ask_volume: int) -> float:
    total = bid_volume + ask_volume
    if total == 0:
        return 0.0
    return (ask_volume - bid_volume) / total


@app.post("/tape")
def add_tape_event(event: TapeEvent):
    delta = compute_delta(event.bid_volume, event.ask_volume)
    imbalance = compute_imbalance(event.bid_volume, event.ask_volume)

    enriched = event.model_dump(mode="json")
    enriched["delta"] = delta
    enriched["imbalance"] = imbalance

    raw = TAPE_PATH.read_text().strip() if TAPE_PATH.exists() else "[]"
    data = json.loads(raw)
    data.append(enriched)

    TAPE_PATH.write_text(json.dumps(data, indent=2))

    return {"status": "ok", "stored": enriched}


@app.get("/tape")
def get_tape_events():
    if not TAPE_PATH.exists():
        return []
    raw = TAPE_PATH.read_text().strip()
    if not raw:
        return []
    return json.loads(raw)
