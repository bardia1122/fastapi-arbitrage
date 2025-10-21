import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings
from app.api.routes import router
from app.db.session import Base, engine, get_db
from app.core.scheduler import Scanner

app = FastAPI(title=settings.APP_NAME)
app.include_router(router, prefix=settings.API_PREFIX)

# CORS
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(o) for o in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

scanner = Scanner(get_db)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    scanner.start()

@app.on_event("shutdown")
async def on_shutdown():
    await scanner.stop()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
