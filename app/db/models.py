from sqlalchemy import Integer, Column, Unicode, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import expression

Base = declarative_base()


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    text = Column(Unicode(length=120), nullable=False)
    is_completed = Column(Boolean, server_default=expression.false())
