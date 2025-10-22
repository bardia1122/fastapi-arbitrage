from typing import List, Dict
import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession
from app.settings import settings
from app.exchanges import nobitex, wallex
from app.db import crud, models
from app.core.metrics import EXCHANGE_LATENCY, EXCHANGE_REQUESTS, ARBITRAGE_EVENTS, LAST_DIFF, ARBITRAGE_VALUE
from app.core.telegram import send_message_telegram
from app.core.bale import send_message_bale

EX_MAP = {"nobitex": nobitex.get_price, "wallex": wallex.get_price}

async def fetch_prices(symbols: List[str]) -> Dict[str, Dict[str, float]]:
    out: Dict[str, Dict[str, float]] = {s: {} for s in symbols}
    async with aiohttp.ClientSession() as sess:
        for s in symbols:
            for ex_name, fn in EX_MAP.items():
                try:
                    t = await fn(sess, s)
                    EXCHANGE_LATENCY.labels(ex_name).observe(t["latency_ms"])
                    EXCHANGE_REQUESTS.labels(ex_name, "ok").inc()
                    out[s][ex_name] = t["price"]
                except Exception:
                    EXCHANGE_REQUESTS.labels(ex_name, "error").inc()
    return out

def normalize_price(symbol: str, exchange: str, price: float) -> float:
    base, quote = symbol.split("-")
    quote = quote.upper()

    if quote in {"IRT", "TMN"}:
        if exchange.lower() == "wallex":
            return price
        elif exchange.lower() == "nobitex":
            return price / 10.0

    return price

async def scan_once(db: AsyncSession) -> int:
    prices = await fetch_prices(settings.SYMBOLS)

    ps = []
    for sym, mp in prices.items():
        for ex, p in mp.items():
            ps.append(models.PriceSnapshot(symbol=sym, exchange=ex, price=p))
    if ps:
        await crud.save_prices(db, ps)

    found = 0
    for sym, mp in prices.items():
        normalized = {
            ex: normalize_price(sym, ex, p)
            for ex, p in mp.items()
        }

        if len(normalized) < 2:
            continue

        buy_ex, buy_price = min(normalized.items(), key=lambda kv: kv[1])
        sell_ex, sell_price = max(normalized.items(), key=lambda kv: kv[1])

        diff_abs = sell_price - buy_price
        if buy_price <= 0:
            continue
        diff_pct = (diff_abs / buy_price) * 100.0

        LAST_DIFF.labels(sym).set(diff_pct)

        if diff_pct >= settings.PROFIT_PCT_THRESHOLD:
            ARBITRAGE_EVENTS.labels(sym).inc()
            ARBITRAGE_VALUE.labels(sym).set(diff_abs)
            
            found += 1

            await crud.insert_opportunity(
                db,
                symbol=sym,
                buy_exchange=buy_ex,
                buy_price=buy_price,
                sell_exchange=sell_ex,
                sell_price=sell_price,
                diff_abs=diff_abs,
                diff_pct=diff_pct,
            )

            msg = (
                f"<b>Arbitrage</b>\n"
                f"• Symbol: <code>{sym}</code>\n"
                f"• Buy @{buy_ex}: {buy_price:,.2f}\n"
                f"• Sell @{sell_ex}: {sell_price:,.2f}\n"
                f"• Diff: {diff_abs:,.2f} ({diff_pct:.2f}%)"
            )
            await send_message_bale(msg)

        print(
            f"[DEBUG] {sym} → Raw: {mp} | Normalized: {normalized} | "
            f"Buy={buy_ex}:{buy_price} Sell={sell_ex}:{sell_price} Diff={diff_pct:.2f}%"
        )

    return found

