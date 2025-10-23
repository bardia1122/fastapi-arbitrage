from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.db.session import get_db
from app.db import crud
from app.schemas.arbitrage import OpportunityOut
from app.core.metrics import (
    EXCHANGE_REQUESTS,
    EXCHANGE_LATENCY,
    ARBITRAGE_EVENTS,
    LAST_DIFF,
    metrics_endpoint,
)
from app.core.arbitrage import scan_once

router = APIRouter()


@router.get("/health")
async def health():
    EXCHANGE_REQUESTS.labels("api", "ok").inc()
    return {"status": "ok"}


@router.get("/metrics")
async def metrics():
    EXCHANGE_REQUESTS.labels("api", "ok").inc()
    return metrics_endpoint()


@router.get("/opportunities", response_model=List[OpportunityOut])
async def get_opps(limit: int = 50, db: AsyncSession = Depends(get_db)):
    res = await crud.recent_opportunities(db, limit=limit)
    EXCHANGE_REQUESTS.labels("api", "ok").inc()
    return res


@router.post("/arbitrage/scan")
async def force_scan(db: AsyncSession = Depends(get_db)):
    """
    اجرای دستی اسکن آربیتراژ (برای تست)
    """
    n = await scan_once(db)
    EXCHANGE_REQUESTS.labels("api", "ok").inc()
    return {"found": n}


@router.get("/prices")
async def last_prices(symbol: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    """
    دریافت آخرین قیمت‌ها از دیتابیس
    """
    res = await crud.last_prices(db, symbol=symbol)
    EXCHANGE_REQUESTS.labels("api", "ok").inc()
    return [
        {
            "id": r.id,
            "symbol": r.symbol,
            "exchange": r.exchange,
            "price": r.price,
            "captured_at": r.captured_at,
        }
        for r in res
    ]
