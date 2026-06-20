from pydantic import BaseModel
from datetime import datetime

class TapeEvent(BaseModel):
    timestamp: datetime
    price: float
    bid_volume: int
    ask_volume: int
    delta: int
    imbalance: float
    notes: str | None = None

TAPE_PATH = Path("tape_reader/tape_storage.json")
