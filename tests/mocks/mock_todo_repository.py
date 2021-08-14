from app.protocols.todo_repository_protocol import TodoNotFoundError
from app.schemas import CreatingTodo, OutTodo, UpdatingTodo


class MockTodoRepository:
    def __init__(self):
        self._last_id = 0
        self._todos: list[OutTodo] = []

    async def create(self, todo: CreatingTodo) -> OutTodo:
        todo = OutTodo(
            id=self._get_id(),
            text=todo.text,
            is_completed=False
        )
        self._todos.append(todo)
        return todo

    async def get_all(self) -> list[OutTodo]:
        return self._todos

    async def get_one_by_id(self, todo_id: int) -> OutTodo:
        try:
            return next(filter(lambda t: t.id == todo_id, self._todos))
        except StopIteration:
            raise TodoNotFoundError(todo_id)

    async def update(self, todo_id: int, todo: UpdatingTodo) -> OutTodo:
        mutable_todo = await self.get_one_by_id(todo_id)

        if todo.text:
            mutable_todo.text = todo.text
        if todo.is_completed:
            mutable_todo.is_completed = todo.is_completed

        return mutable_todo

    async def delete(self, todo_id: int) -> OutTodo:
        todo = await self.get_one_by_id(todo_id)
        index = self._todos.index(todo)

        todo = todo.copy()

        del self._todos[index]
        return todo

    def _get_id(self):
        self._last_id += 1
        return self._last_id

    def clear(self):
        self._todos = []
        self._last_id = 0
