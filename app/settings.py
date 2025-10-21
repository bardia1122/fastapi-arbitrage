from pydantic import AnyHttpUrl
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "Arbitrage Service")
    API_PREFIX: str = os.getenv("API_PREFIX")
    HOST: str = os.getenv("HOST")
    PORT: int = int(os.getenv("PORT"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    SYMBOLS: List[str] = os.getenv("SYMBOLS", "USDT-IRT,BTC-USDT").split(",")
    SCAN_INTERVAL_SEC: int = int(os.getenv("SCAN_INTERVAL_SEC", 7))
    PROFIT_PCT_THRESHOLD: float = float(os.getenv("PROFIT_PCT_THRESHOLD", 0.5))

    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")

    DATABASE_URL: str = os.getenv("DATABASE_URL")

    CORS_ORIGINS: List[AnyHttpUrl] = []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
