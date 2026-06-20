import json
from pathlib import Path

DIARY_PATH = Path("diary/diary_storage.json")

def load_entries():
    if not DIARY_PATH.exists():
        return []
    raw = DIARY_PATH.read_text().strip()
    return json.loads(raw) if raw else []

def save_entries(entries):
    DIARY_PATH.write_text(json.dumps(entries, indent=2))