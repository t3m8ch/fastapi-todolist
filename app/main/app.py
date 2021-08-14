from fastapi import FastAPI

from .config import AppConfig
from .events_handling import create_startup_handler, create_shutdown_handler
from ..endpoints import include_routers


def get_app() -> FastAPI:
    config = AppConfig()

    app = FastAPI()

    app.add_event_handler("startup", create_startup_handler(app, config.db_url))
    app.add_event_handler("shutdown", create_shutdown_handler(app))

    include_routers(app)

    return app