from sqlmodel import SQLModel, Field, Relationship, Column, DateTime

from typing import Optional, List

class User(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True, index=True)
    name: str