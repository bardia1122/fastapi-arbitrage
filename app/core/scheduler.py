import asyncio, logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.settings import settings
from app.core.arbitrage import scan_once

log = logging.getLogger(__name__)

class Scanner:
    def __init__(self, db_factory):
        self._db_factory = db_factory
        self._task: asyncio.Task | None = None
        self._stop = asyncio.Event()

    async def _runner(self):
        while not self._stop.is_set():
            try:
                async for db in self._db_factory():
                    found = await scan_once(db)
            except Exception as e:
                log.exception(f"Error in scanner loop: {e}")
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=settings.SCAN_INTERVAL_SEC)
            except asyncio.TimeoutError:
                continue

    def start(self):
        if self._task is None or self._task.done():
            self._stop.clear()
            self._task = asyncio.create_task(self._runner())

    async def stop(self):
        self._stop.set()
        if self._task:
            await self._task
