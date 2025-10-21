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
        log.info("Scanner started (interval=%ds)", settings.SCAN_INTERVAL_SEC)
        while not self._stop.is_set():
            try:
                async for db in self._db_factory():
                    found = await scan_once(db)
                    log.info(f"scan_once() completed → found {found} opportunities")
            except Exception as e:
                log.exception(f"Error in scanner loop: {e}")
            # Wait before next iteration
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=settings.SCAN_INTERVAL_SEC)
            except asyncio.TimeoutError:
                continue
        log.info("Scanner stopped")

    def start(self):
        if self._task is None or self._task.done():
            self._stop.clear()
            self._task = asyncio.create_task(self._runner())
            log.info("Scanner background task created")

    async def stop(self):
        log.info("Stopping scanner...")
        self._stop.set()
        if self._task:
            await self._task
            log.info("Scanner fully stopped")
