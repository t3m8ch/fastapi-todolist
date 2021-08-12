import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from app.db.models import Base
from app.endpoints import include_routers

app = FastAPI()
include_routers(app)


@app.on_event("startup")
async def startup():
    engine = create_async_engine(
        "postgresql+asyncpg://localhost/fastapi"
    )
    app.state.alchemy_engine = engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await app.state.alchemy_engine.dispose()


if __name__ == '__main__':
    uvicorn.run("app.__main__:app", reload=True)
