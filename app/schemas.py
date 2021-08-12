from typing import Optional

from pydantic import BaseModel


class OutTodo(BaseModel):
    id: int
    text: str
    is_completed: bool


class CreatingTodo(BaseModel):
    text: str


class UpdatingTodo(BaseModel):
    text: Optional[str]
    is_completed: Optional[bool]
