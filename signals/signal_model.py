from pydantic import BaseModel
from datetime import datetime

class Signal(BaseModel):
    timestamp: datetime
    signal_type: str
    description: str
    strength: int | None = None
    metadata: dict | None = None


import json
from pathlib import Path

STORAGE_PATH = Path(__file__).parent / "signal_storage.json"


def load_signals():
    if STORAGE_PATH.exists():
        with open(STORAGE_PATH, "r") as f:
            return json.load(f)
        return {}
   
       
def save_signals(signals):
    with open(STORAGE_PATH, "w") as f:
        json.dump(signals, f, indent=4)
