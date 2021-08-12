import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine

from app.__main__ import get_app
from app.config import AppConfig
from app.db.init_db import init_db, create_engine


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def engine() -> AsyncEngine:
    config = AppConfig()

    engine = create_engine(config.test_db_url)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="module")
def client(engine: AsyncEngine) -> TestClient:
    app = get_app()
    app.state.alchemy_engine = engine
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def init_db_fixture(engine: AsyncEngine):
    asyncio.get_event_loop().run_until_complete(init_db(engine))


def test_create_todo(client: TestClient):
    response1 = client.post("/todos", json={"text": "first"})
    response2 = client.post("/todos", json={"text": "second"})
    response3 = client.post("/todos", json={"text": "third"})

    assert all(res.status_code == 200
               for res in (response1, response2, response3))

    assert response1.json() == {
        "id": 1,
        "text": "first",
        "is_completed": False
    }
    assert response2.json() == {
        "id": 2,
        "text": "second",
        "is_completed": False
    }
    assert response3.json() == {
        "id": 3,
        "text": "third",
        "is_completed": False
    }
