import time, aiohttp
from app.exchanges.types import Ticker
from app.exchanges.symbols import normalize_for_wallex

BASE = "https://api.wallex.ir"

async def get_price(session: aiohttp.ClientSession, symbol: str) -> Ticker:

    sym = normalize_for_wallex(symbol)
    t0 = time.perf_counter()
    async with session.get(f"{BASE}/v1/markets") as resp:
        data = await resp.json()
    latency_ms = (time.perf_counter() - t0)


    info = data["result"]["symbols"][sym]
    last_price = float(info["stats"]["lastPrice"])
    return {"symbol": symbol, "price": last_price, "exchange": "wallex", "latency_ms": latency_ms}
