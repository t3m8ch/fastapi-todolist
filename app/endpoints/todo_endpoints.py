from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_repository
from app.protocols.todo_repository_protocol import TodoRepositoryProtocol
from app.schemas import OutTodo, CreatingTodo, UpdatingTodo
from app.services.todo_repository import TodoRepository, TodoNotFoundError

todo_router = APIRouter()


@todo_router.post("/todos", response_model=OutTodo)
async def create_todo(
        todo: CreatingTodo,
        todo_repository: TodoRepositoryProtocol = Depends(
            get_repository(TodoRepository))
):
    return await todo_repository.create(todo)


@todo_router.get("/todos", response_model=list[OutTodo])
async def get_all_todos(
        todo_repository: TodoRepositoryProtocol = Depends(
            get_repository(TodoRepository))
):
    return await todo_repository.get_all()


@todo_router.get("/todos/{todo_id}", response_model=OutTodo)
async def get_todo_by_id(
        todo_id: int,
        todo_repository: TodoRepositoryProtocol = Depends(
            get_repository(TodoRepository))
):
    try:
        return await todo_repository.get_one_by_id(todo_id)
    except TodoNotFoundError:
        raise HTTPException(404, "Todo not found")


@todo_router.put("/todos/{todo_id}", response_model=OutTodo)
async def update_todo(
        todo_id: int,
        todo: UpdatingTodo,
        todo_repository: TodoRepositoryProtocol = Depends(
            get_repository(TodoRepository))
):
    try:
        return await todo_repository.update(todo_id, todo)
    except TodoNotFoundError:
        raise HTTPException(404, "Todo not found")


@todo_router.delete("/todos/{todo_id}", response_model=OutTodo)
async def delete_todo(
        todo_id: int,
        todo_repository: TodoRepositoryProtocol = Depends(
            get_repository(TodoRepository))
):
    try:
        return await todo_repository.delete(todo_id)
    except TodoNotFoundError:
        raise HTTPException(404, "Todo not found")
