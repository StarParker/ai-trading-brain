import json
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path


class DiaryEntry(BaseModel):
    date: datetime
    htf_bias: str
    key_levels: list[str]
    scenarios: list[str]
    notess: str


STORAGE_PATH = Path(__file__).parent / "diary_storage.json"


def load_entries():
    if STORAGE_PATH.exists():
        with open(STORAGE_PATH, "r") as f:
            data = json.load(f)
            # Convert date strings back to datetime objects
            for entry in data:
                if isinstance(entry.get('date'), str):
                    entry['date'] = datetime.fromisoformat(entry['date'])
            return data
    return []


def save_entries(entries):
    # Convert datetime objects to ISO format strings for JSON serialization
    entries_to_save = []
    for entry in entries:
        entry_copy = entry.copy() if isinstance(entry, dict) else entry.dict()
        if isinstance(entry_copy.get('date'), datetime):
            entry_copy['date'] = entry_copy['date'].isoformat()
        entries_to_save.append(entry_copy)
    
    with open(STORAGE_PATH, "w") as f:
        json.dump(entries_to_save, f, indent=4)
