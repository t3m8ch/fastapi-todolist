from typing import Protocol

from app.schemas import CreatingTodo, OutTodo, UpdatingTodo


class TodoRepositoryProtocol(Protocol):
    async def create(self, todo: CreatingTodo) -> OutTodo:
        pass

    async def get_all(self) -> list[OutTodo]:
        pass

    async def get_one_by_id(self, todo_id: int) -> OutTodo:
        pass

    async def update(self, todo_id: int, todo: UpdatingTodo) -> OutTodo:
        pass

    async def delete(self, todo_id: int) -> OutTodo:
        pass
