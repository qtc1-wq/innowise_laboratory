"""
Pydantic models for request validation and response formatting.
"""

from typing import Optional
from pydantic import BaseModel, Field


class BookBase(BaseModel):
    """
    Base model shared across Create / Update / Output schemas.
    """
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    year: Optional[int] = Field(None, ge=0)


class BookCreate(BookBase):
    """
    Request body for creating a new book.
    """
    pass


class BookUpdate(BaseModel):
    """
    Request body for updating book fields.
    """
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = Field(None, ge=0)


class BookOut(BookBase):
    """
    Response model returned.
    """
    id: int

    model_config = {
        "from_attributes": True
    }
