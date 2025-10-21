# app/models.py (or wherever your models live)
from typing import Optional, List
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON  # <- use the SQLite dialect JSON

class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    # Important bits:
    # - Annotate as List[str] (not plain list) so Pydantic knows the inner type
    # - Give SQLAlchemy a real JSON column via sa_column
    # - Use default_factory=list to avoid mutable default pitfalls
    tags: List[str] = Field(default_factory=list, sa_column=Column(SQLiteJSON))
