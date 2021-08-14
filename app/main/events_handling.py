from typing import Callable

from fastapi import FastAPI

from app.db.init_db import init_db, create_engine


def create_startup_handler(app: FastAPI, db_url: str) -> Callable:
    async def startup() -> None:
        engine = create_engine(db_url)
        await init_db(engine)
        app.state.alchemy_engine = engine

    return startup


def create_shutdown_handler(app: FastAPI) -> Callable:
    async def shutdown() -> None:
        await app.state.alchemy_engine.dispose()

    return shutdown
