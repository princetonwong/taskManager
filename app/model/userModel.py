from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from uuid import uuid4, UUID


class UserBase(SQLModel):
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    created_tasks: List["Task"] = Relationship(back_populates="created_by_user")
    updated_tasks: List["Task"] = Relationship(back_populates="updated_by_user")


class User(UserBase, table=True):
    id: UUID = Field(primary_key=True, index=True)