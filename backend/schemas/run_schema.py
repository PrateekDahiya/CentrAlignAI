"""Pydantic schemas: runs."""
from datetime import datetime
from pydantic import BaseModel


class RunCreate(BaseModel):
    task: str


class RunOut(BaseModel):
    id: str
    task: str
    status: str


class RunListOut(BaseModel):
    id: str
    task: str
    status: str
    created_at: datetime | None = None
