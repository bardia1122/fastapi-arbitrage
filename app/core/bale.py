import aiohttp
from app.settings import settings

async def send_message_bale(text: str) -> None:
    if not settings.BALE_BOT_TOKEN or not settings.BALE_CHAT_ID:
        return
    url = f"https://tapi.bale.ai/bot{settings.BALE_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": settings.BALE_CHAT_ID, "text": text, "parse_mode": "HTML"}
    async with aiohttp.ClientSession() as s:
        async with s.post(url, json=payload) as _:
            return
