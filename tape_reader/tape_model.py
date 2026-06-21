from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class LiquidityChange(BaseModel):
    bid: float
    ask: float


class FootprintCell(BaseModel):
    volume: float
    delta: float
    imbalance: float


class TapeEvent(BaseModel):
    # --- Core tape fields ---
    timestamp: datetime
    symbol: str
    price: float

    # --- Prints / Time & Sales ---
    last_trade_size: Optional[float] = None
    aggressor: Optional[str] = None  # "buy" or "sell"

    # --- Volume / Delta / Imbalance ---
    bid_volume: float
    ask_volume: float
    delta: Optional[float] = None
    imbalance: Optional[float] = None

    # --- DOM Depth (top 5 levels recommended) ---
    bid_depth: Optional[List[float]] = None
    ask_depth: Optional[List[float]] = None

    # --- Microstructure Flags ---
    sweep_flag: Optional[bool] = None
    iceberg_flag: Optional[bool] = None

    # --- Liquidity Behavior ---
    liquidity_pull: Optional[LiquidityChange] = None
    liquidity_add: Optional[LiquidityChange] = None

    # --- Footprint Cell Data ---
    footprint_bid: Optional[FootprintCell] = None
    footprint_ask: Optional[FootprintCell] = None

    # --- Contextual Tags ---
    session: Optional[str] = None      # "RTH", "ON", etc.
    level_tag: Optional[str] = None    # "ONH", "ONL", "IBH", "IBL", "VWAP", etc.

    # --- Notes (optional) ---
    notes: Optional[str] = None
