from fastapi import FastAPI

from .todo_endpoints import todo_router

__all__ = ["include_routers"]


def include_routers(app: FastAPI):
    app.include_router(todo_router)
