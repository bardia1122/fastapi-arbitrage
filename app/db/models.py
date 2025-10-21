from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from sqlalchemy.sql import func
from app.db.session import Base

class Opportunity(Base):
    __tablename__ = "opportunities"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(32), index=True)
    buy_exchange = Column(String(16))
    buy_price = Column(Float)
    sell_exchange = Column(String(16))
    sell_price = Column(Float)
    diff_abs = Column(Float)         # sell - buy
    diff_pct = Column(Float)         # (sell-buy)/buy * 100
    detected_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

Index("ix_opps_symbol_time", Opportunity.symbol, Opportunity.detected_at.desc())

class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(32), index=True)
    exchange = Column(String(16), index=True)
    price = Column(Float)
    captured_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

Index("ix_prices_symbol_exchange_time", PriceSnapshot.symbol, PriceSnapshot.exchange, PriceSnapshot.captured_at.desc())
