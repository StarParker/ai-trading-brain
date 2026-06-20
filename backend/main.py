# import lines
from fastapi import FastAPI
from diary.diary_model import DiaryEntry, load_entries, save_entries
from signals.signal_model import Signal, STORAGE_PATH
from tape_reader.tape_model import TapeEvent
from pathlib import Path
import json


app = FastAPI()


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


@app.post("/tape")
def add_tape_event(event: TapeEvent):
    raw = TAPE_PATH.read_text().strip() if TAPE_PATH.exists() else "[]"
    data = json.loads(raw)
    data.append(event.dict())
    TAPE_PATH.write_text(json,.dumps(data, indent=2))return {"status": "ok", "stored": event}


@app.get("/tape")
def get_tape_events():
    if not TAPE_PATH.exists():
        return []
    raw = TAPE_PATH.read_text().strip()
    if not raw:
        return []
    return json.loads(raw)
