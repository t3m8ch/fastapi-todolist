import asyncio

from fastapi.testclient import TestClient

from app.__main__ import get_app
from app.config import AppConfig
from app.db.init_db import init_db

config = AppConfig()
app = get_app()

client = TestClient(app)


def test_create_todo():
    app.state.alchemy_engine = asyncio.get_event_loop().run_until_complete(
        init_db(config.test_db_url)
    )

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
