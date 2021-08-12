from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from .models import Base


def create_engine(db_url: str) -> AsyncEngine:
    return create_async_engine(db_url)


async def init_db(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
