import time, aiohttp
from app.exchanges.types import Ticker
from app.exchanges.symbols import normalize_for_nobitex

BASE = "https://apiv2.nobitex.ir"

USER_AGENT = "TraderBot/ARB-Scanner"

async def get_price(session: aiohttp.ClientSession, symbol: str) -> Ticker:
    sym = normalize_for_nobitex(symbol)
    t0 = time.perf_counter()
    async with session.get(f"{BASE}/v3/orderbook/{sym}", headers={"User-Agent": USER_AGENT}) as resp:
        data = await resp.json()
    latency_ms = (time.perf_counter() - t0) * 1000

    last_trade = float(data.get("lastTradePrice"))
    return {"symbol": symbol, "price": last_trade, "exchange": "nobitex", "latency_ms": latency_ms}
