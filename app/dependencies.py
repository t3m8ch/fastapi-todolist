from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.services.todo_repository import TodoRepository


async def _get_alchemy_session(request: Request):
    session = AsyncSession(request.app.state.alchemy_engine)
    try:
        yield session
    finally:
        await session.close()


def get_todo_repository(
        alchemy_session: AsyncSession = Depends(_get_alchemy_session)
):
    return TodoRepository(alchemy_session)
