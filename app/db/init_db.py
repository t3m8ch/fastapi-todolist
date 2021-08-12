from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from .models import Base


async def init_db(db_url: str) -> AsyncEngine:
    engine = create_async_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return engine
