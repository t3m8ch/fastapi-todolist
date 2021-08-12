from fastapi import APIRouter, Depends

from app.dependencies import get_repository
from app.schemas import OutTodo, CreatingTodo, UpdatingTodo
from app.services.todo_repository import TodoRepository

todo_router = APIRouter()


@todo_router.post("/todos", response_model=OutTodo)
async def create_todo(
        todo: CreatingTodo,
        todo_repository: TodoRepository = Depends(
            get_repository(TodoRepository))
):
    return await todo_repository.create(todo)


@todo_router.get("/todos", response_model=list[OutTodo])
async def get_all_todos():
    pass


@todo_router.get("/todos/{todo_id}", response_model=OutTodo)
async def get_todo_by_id(todo_id: int):
    pass


@todo_router.put("/todos/{todo_id}", response_model=OutTodo)
async def update_todo(todo_id: int, todo: UpdatingTodo):
    pass


@todo_router.delete("/todos/{todo_id}", response_model=OutTodo)
async def delete_todo(todo_id: int):
    pass
