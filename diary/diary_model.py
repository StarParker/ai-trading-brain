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
            return json.load(f)
        return []


def save_entries(entries):
    with open(STORAGE_PATH, "w") as f:
        json.dump(entries, f, indent=4)
