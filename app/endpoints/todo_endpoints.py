from fastapi import APIRouter

from app.schemas import OutTodo, CreatingTodo, UpdatingTodo

todo_router = APIRouter()


@todo_router.post("/todos", response_model=OutTodo)
async def create_todo(todo: CreatingTodo):
    pass


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
