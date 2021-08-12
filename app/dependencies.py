from typing import Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.services.base_repository import BaseRepository


async def _get_alchemy_session(request: Request):
    session = AsyncSession(request.app.state.alchemy_engine)
    try:
        yield session
    finally:
        await session.close()


def get_repository(repository_type: Type[BaseRepository]):
    def func(alchemy_session: AsyncSession = Depends(_get_alchemy_session)):
        return repository_type(alchemy_session)

    return func
