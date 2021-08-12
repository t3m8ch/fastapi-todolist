from typing import Callable

from fastapi import FastAPI

from app.db.init_db import init_db


def create_startup_handler(app: FastAPI, db_url: str) -> Callable:
    async def startup() -> None:
        app.state.alchemy_engine = await init_db(db_url)

    return startup


def create_shutdown_handler(app: FastAPI) -> Callable:
    async def shutdown() -> None:
        await app.state.alchemy_engine.dispose()

    return shutdown
