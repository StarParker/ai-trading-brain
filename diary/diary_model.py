from pydantic import BaseModel
from datetime import datetime

class DiaryEntry(BaseModel):
    date: datetime
    htf_bias: str
    key_levels: list[str]
    scenarios: list[str]
    notess: str
    