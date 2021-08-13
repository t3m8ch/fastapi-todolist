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
async def init_db_fixture(engine: AsyncEngine):
    await init_db(engine)


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


def test_get_all_todos(client: TestClient):
    client.post("/todos", json={"text": "first"})
    client.post("/todos", json={"text": "second"})
    client.post("/todos", json={"text": "third"})

    all_todos = client.get("/todos").json()

    assert all_todos == [
        {
            "id": 1,
            "text": "first",
            "is_completed": False
        },
        {
            "id": 2,
            "text": "second",
            "is_completed": False
        },
        {
            "id": 3,
            "text": "third",
            "is_completed": False
        },
    ]


def test_get_all_todos_if_there_not_todos(client: TestClient):
    all_todos = client.get("/todos").json()
    assert all_todos == []


def test_get_todo_by_id(client: TestClient):
    client.post("/todos", json={"text": "first"})
    client.post("/todos", json={"text": "second"})

    assert client.get("/todos/1").json() == {
        "id": 1,
        "text": "first",
        "is_completed": False
    }
    assert client.get("/todos/2").json() == {
        "id": 2,
        "text": "second",
        "is_completed": False
    }


def test_get_todo_by_id_if_todo_not_found(client: TestClient):
    client.post("/todos", json={"text": "first"})
    client.post("/todos", json={"text": "second"})

    response = client.get("/todos/50")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Todo not found"
    }


def test_update_todo(client: TestClient):
    client.post("/todos", json={"text": "first"})
    client.post("/todos", json={"text": "second"})
    client.post("/todos", json={"text": "third"})
    client.post("/todos", json={"text": "fourth"})

    update1 = client.put("/todos/1", json={"is_completed": True})
    update2 = client.put("/todos/2", json={"text": "something"})
    update3 = client.put("/todos/3", json={
        "text": "something",
        "is_completed": True
    })

    assert all(u.status_code == 200 for u in (update1, update2, update3))

    assert sorted(client.get("/todos").json(), key=lambda i: i["id"]) == [
        {
            "id": 1,
            "text": "first",
            "is_completed": True
        },
        {
            "id": 2,
            "text": "something",
            "is_completed": False
        },
        {
            "id": 3,
            "text": "something",
            "is_completed": True
        },
        {
            "id": 4,
            "text": "fourth",
            "is_completed": False
        }
    ]


def test_update_todo_if_todo_not_found(client: TestClient):
    expected = client.put("/todos/50", json={"is_completed": True})
    assert expected.status_code == 404
    assert expected.json() == {
        "detail": "Todo not found"
    }


def test_delete_todo(client: TestClient):
    client.post("/todos", json={"text": "first"})
    client.post("/todos", json={"text": "second"})

    client.delete("todos/1")

    actual = client.get("/todos").json()

    assert len(actual) == 1
    assert actual == [
        {
            "id": 2,
            "text": "second",
            "is_completed": False
        }
    ]


def test_delete_todo_if_todo_not_found(client: TestClient):
    actual = client.delete("/todos/50")

    assert actual.status_code == 404
    assert actual.json() == {
        "detail": "Todo not found"
    }
