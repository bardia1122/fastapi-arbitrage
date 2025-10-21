from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Opportunity, PriceSnapshot

async def save_prices(db: AsyncSession, prices: List[PriceSnapshot]) -> None:
    db.add_all(prices)
    await db.commit()

async def insert_opportunity(
    db: AsyncSession,
    *,
    symbol: str,
    buy_exchange: str,
    buy_price: float,
    sell_exchange: str,
    sell_price: float,
    diff_abs: float,
    diff_pct: float,
) -> Opportunity:
    opp = Opportunity(
        symbol=symbol, buy_exchange=buy_exchange, buy_price=buy_price,
        sell_exchange=sell_exchange, sell_price=sell_price,
        diff_abs=diff_abs, diff_pct=diff_pct
    )
    db.add(opp)
    await db.commit()
    await db.refresh(opp)
    return opp

async def recent_opportunities(db: AsyncSession, limit: int = 50) -> List[Opportunity]:
    q = select(Opportunity).order_by(Opportunity.detected_at.desc()).limit(limit)
    res = await db.execute(q)
    return list(res.scalars())

async def last_prices(db: AsyncSession, symbol: Optional[str] = None, limit: int = 100):
    q = select(PriceSnapshot).order_by(PriceSnapshot.captured_at.desc())
    if symbol:
        q = q.where(PriceSnapshot.symbol == symbol)
    q = q.limit(limit)
    res = await db.execute(q)
    return list(res.scalars())
