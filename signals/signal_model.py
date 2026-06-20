from pydantic import BaseModel
from datetime import datetime
from pathlib import Path

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

STORAGE_PATH = Path(__file__).parent / "signal_storage.json"