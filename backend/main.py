# import lines
from fastapi import FastAPI
from diary.diary_model import DiaryEntry, load_entries, save_entries
from signals.signal_model import Signal, STORAGE_PATH
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