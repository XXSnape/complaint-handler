import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import aiohttp
import uvicorn
from aiohttp import ClientTimeout
from api import router as api_router
from core.config import settings
from core.models import db_helper
from fastapi import FastAPI

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Устанавливает сессию для aiohttp и сбрасывает соединение
    с базой данных после завершения работы приложения.
    """
    async with aiohttp.ClientSession(
        headers={"apikey": settings.resources.sentinel.key},
        timeout=ClientTimeout(total=10),
    ) as client_session:
        app.state.client_session = client_session
        yield
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
)
main_app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
