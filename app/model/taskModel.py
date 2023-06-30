from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime
from uuid import uuid4, UUID


class TaskBase(SQLModel):
    name: str = Field(default=None, index=True)
    description: str
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    last_edited: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # created_by: int = Field(foreign_key="user.id")
    # last_updated_by: int = Field(foreign_key="user.id")
    # created_by_user: Optional[User] = Relationship(back_populates="created_tasks")
    # last_updated_by_user: Optional[User] = Relationship(back_populates="updated_tasks")


class Task(TaskBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: UUID


class TaskUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    # created_by: Optional[int] = None
