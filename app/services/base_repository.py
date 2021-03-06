from sqlalchemy.ext.asyncio import AsyncSession


class AlchemySessionMixin:
    def __init__(self, alchemy_session: AsyncSession):
        self._session = alchemy_session
