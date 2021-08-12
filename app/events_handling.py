from typing import Callable

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from app.db.models import Base


def create_startup_handler(app: FastAPI, db_url: str) -> Callable:
    async def startup() -> None:
        engine = create_async_engine(db_url)
        app.state.alchemy_engine = engine

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    return startup


def create_shutdown_handler(app: FastAPI) -> Callable:
    async def shutdown() -> None:
        await app.state.alchemy_engine.dispose()

    return shutdown
