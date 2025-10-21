from typing import TypedDict

class Ticker(TypedDict):
    symbol: str
    price: float
    exchange: str
    latency_ms: float
