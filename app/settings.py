from pydantic import AnyHttpUrl
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
class Settings(BaseSettings):
    APP_NAME: str = "Arbitrage Service"
    API_PREFIX: str = "/api"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    SYMBOLS: List[str] = ["USDT-IRT", "BTC-USDT"]
    SCAN_INTERVAL_SEC: int = int(os.getenv("SCAN_INTERVAL_SEC", 7))
    PROFIT_PCT_THRESHOLD: float = float(os.getenv("PROFIT_PCT_THRESHOLD", 0.5))

    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")

    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/arb"

    CORS_ORIGINS: List[AnyHttpUrl] = []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
