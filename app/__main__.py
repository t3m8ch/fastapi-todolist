import uvicorn
from fastapi import FastAPI

from app.config import AppConfig
from app.endpoints import include_routers
from app.events_handling import create_startup_handler, create_shutdown_handler


def get_app() -> FastAPI:
    config = AppConfig()

    app = FastAPI()

    app.add_event_handler("startup", create_startup_handler(app, config.db_url))
    app.add_event_handler("shutdown", create_shutdown_handler(app))

    include_routers(app)

    return app


app = get_app()

if __name__ == "__main__":
    uvicorn.run("app.__main__:app", reload=True)
