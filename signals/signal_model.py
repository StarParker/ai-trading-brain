from pydantic import BaseModel
from datetime import datetime
import json
from pathlib import Path

# -----------------------------------
# Expanded Signal Model
# -----------------------------------


class Signal(BaseModel):
    timestamp: datetime
    signal_type: str
    category: str | None = None
    strength: int | None = None
    playbook_tag: str | None = None
    htf_bias: str | None = None
    ltf_context: str | None = None
    trigger: str | None = None
    invalidation: str | None = None
    metadata: dict | None = None


# -----------------------------------
# Storage Helpers
# -----------------------------------


STORAGE_PATH = Path(__file__).parent / "signal_storage.json"


def load_signals():
    if STORAGE_PATH.exists():
        with open(STORAGE_PATH, "r") as f:
            return json.load(f)
        return []


def save_signals(signals):
    with open(STORAGE_PATH, "w") as f:
        json.dump(signals, f, indent=4)
