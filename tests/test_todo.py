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
    actual_responses = [
        client.post("/todos", json={"text": "first"}),
        client.post("/todos", json={"text": "second"}),
        client.post("/todos", json={"text": "third"})
    ]

    assert all(r.status_code == 200 for r in actual_responses)

    assert actual_responses[0].json() == {
        "id": 1,
        "text": "first",
        "is_completed": False
    }
    assert actual_responses[1].json() == {
        "id": 2,
        "text": "second",
        "is_completed": False
    }
    assert actual_responses[2].json() == {
        "id": 3,
        "text": "third",
        "is_completed": False
    }


def test_get_all_todos(client: TestClient):
    client.post("/todos", json={"text": "first"})
    client.post("/todos", json={"text": "second"})
    client.post("/todos", json={"text": "third"})

    actual_response = client.get("/todos")

    assert actual_response.status_code == 200
    assert actual_response.json() == [
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
    actual_response = client.get("/todos")

    assert actual_response.status_code == 200
    assert actual_response.json() == []


def test_get_todo_by_id(client: TestClient):
    client.post("/todos", json={"text": "first"})
    client.post("/todos", json={"text": "second"})

    actual_responses = [client.get("/todos/1"), client.get("/todos/2")]

    assert all(r.status_code == 200 for r in actual_responses)

    assert actual_responses[0].json() == {
        "id": 1,
        "text": "first",
        "is_completed": False
    }
    assert actual_responses[1].json() == {
        "id": 2,
        "text": "second",
        "is_completed": False
    }


def test_get_todo_by_id_if_todo_not_found(client: TestClient):
    client.post("/todos", json={"text": "first"})
    client.post("/todos", json={"text": "second"})

    actual_response = client.get("/todos/50")
    assert actual_response.status_code == 404
    assert actual_response.json() == {
        "detail": "Todo not found"
    }


def test_update_todo(client: TestClient):
    client.post("/todos", json={"text": "first"})
    client.post("/todos", json={"text": "second"})
    client.post("/todos", json={"text": "third"})
    client.post("/todos", json={"text": "fourth"})

    expected_todos = [
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

    actual_responses = [
        client.put("/todos/1", json={"is_completed": True}),
        client.put("/todos/2", json={"text": "something"}),
        client.put("/todos/3", json={
            "text": "something",
            "is_completed": True
        })
    ]
    actual_todos = sorted(client.get("/todos").json(), key=lambda i: i["id"])

    assert all(r.status_code == 200 for r in actual_responses)
    assert actual_todos == expected_todos
    assert all(expected_todos[i] == actual_todos[i] for i in range(4))


def test_update_todo_if_todo_not_found(client: TestClient):
    actual_response = client.put("/todos/50", json={"is_completed": True})
    assert actual_response.status_code == 404
    assert actual_response.json() == {
        "detail": "Todo not found"
    }


def test_delete_todo(client: TestClient):
    client.post("/todos", json={"text": "first"})
    client.post("/todos", json={"text": "second"})

    client.delete("todos/1")

    actual_response = client.get("/todos")
    json = actual_response.json()

    assert actual_response.status_code == 200
    assert len(json) == 1
    assert json == [
        {
            "id": 2,
            "text": "second",
            "is_completed": False
        }
    ]


def test_delete_todo_if_todo_not_found(client: TestClient):
    actual_response = client.delete("/todos/50")

    assert actual_response.status_code == 404
    assert actual_response.json() == {
        "detail": "Todo not found"
    }
