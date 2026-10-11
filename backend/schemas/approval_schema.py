"""Pydantic schemas: approval gate."""
from pydantic import BaseModel


class ApprovalIn(BaseModel):
    approved: bool
    answer: str = ""
