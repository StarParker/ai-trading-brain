from pydantic import BaseModel
from datetime import datetime

class TapeEvent(BaseModel):
    timestamp: datetime
    price: float
    bid_volume: int
    ask_volume: int
    delta: int | None = None
    imbalance: float | None = None
    notes: str | None = None
