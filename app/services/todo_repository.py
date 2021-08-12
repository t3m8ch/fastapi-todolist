from sqlalchemy import insert, select, update
from sqlalchemy.exc import NoResultFound

from app.db.models import Todo
from app.schemas import OutTodo, CreatingTodo, UpdatingTodo
from app.services.base_repository import BaseRepository


class TodoNotFoundError(Exception):
    def __init__(self, todo_id: int):
        self.todo_id = todo_id


class TodoRepository(BaseRepository):
    async def create(self, todo: CreatingTodo) -> OutTodo:
        todo = (await self._session.execute(
            insert(Todo).values(text=todo.text).
            returning(Todo)
        )).one()
        await self._session.commit()

        return _map_todo_to_pydantic(todo)

    async def get_all(self) -> list[OutTodo]:
        todos = (await self._session.execute(select(Todo))).scalars().all()
        return list(map(_map_todo_to_pydantic, todos))

    async def get_one_by_id(self, todo_id: int) -> OutTodo:
        if not (todo := await self._session.get(Todo, todo_id)):
            raise TodoNotFoundError(todo_id)

        return _map_todo_to_pydantic(todo)

    async def update(self, todo_id: int, todo: UpdatingTodo) -> OutTodo:
        todo = await self._execute_update_query(todo_id, todo)
        await self._session.commit()
        return _map_todo_to_pydantic(todo)

    async def _execute_update_query(
            self,
            todo_id: int,
            todo: UpdatingTodo
    ) -> Todo:
        # Uncle Bob says that exception handling should be moved
        # to a separate method
        try:
            return (await self._session.execute(
                update(Todo).where(Todo.id == todo_id).
                values(**todo.dict(exclude_none=True)).
                returning(Todo)
            )).one()
        except NoResultFound:
            raise TodoNotFoundError(todo_id)

def _map_todo_to_pydantic(table: Todo) -> OutTodo:
    return OutTodo(
        id=table.id,
        text=table.text,
        is_completed=table.is_completed
    )
