from pydantic import BaseModel
from datetime import datetime

class OpportunityOut(BaseModel):
    id: int
    symbol: str
    buy_exchange: str
    buy_price: float
    sell_exchange: str
    sell_price: float
    diff_abs: float
    diff_pct: float
    detected_at: datetime

    class Config:
        from_attributes = True
