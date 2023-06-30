from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from uuid import uuid4, UUID


class TaskBase(SQLModel):
    name: str = Field(default=None, index=True)
    description: str
    done: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    last_edited: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    created_by: UUID = Field(foreign_key="user.id")
    # last_updated_by: UUID = Field(foreign_key="user.id")
    created_by_user: Optional["User"] = Relationship(back_populates="created_tasks")
    # last_updated_by_user: Optional["User"] = Relationship(back_populates="updated_tasks")


class Task(TaskBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)


class TaskCreate(TaskBase):
    created_by: UUID


class TaskRead(TaskBase):
    id: UUID


class TaskUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    # updated_by: Optional[int] = None
