"""Pydantic schemas: runs."""
from pydantic import BaseModel


class RunCreate(BaseModel):
    task: str


class RunOut(BaseModel):
    id: str
    task: str
    status: str
