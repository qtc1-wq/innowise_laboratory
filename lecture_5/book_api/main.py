"""

FastAPI application for Simple Book Collection API.

Endpoints:
- POST /books/           Create a book
- GET  /books/           List all books
- GET  /books/search/    Search books by title/author/year
- PUT  /books/{book_id}  Update a book
- DELETE /books/{book_id} Delete a book
"""

from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, engine, get_db

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Simple Book Collection API",
    description="API for storing and managing books using FastAPI + SQLAlchemy ORM.",
)


@app.get("/")
def root() -> dict:
    """
    Simple greeting route to avoid 404 on the root path.
    """
    return {"message": "Welcome to the Book API. Visit /docs for interactive documentation."}


@app.post("/books/", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book_in: schemas.BookCreate, db: Session = Depends(get_db)) -> schemas.BookOut:
    """
    Create a new book in the database.
    """
    book = models.Book(**book_in.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.get("/books/", response_model=List[schemas.BookOut])
def list_books(db: Session = Depends(get_db)) -> List[schemas.BookOut]:
    """
    Return all books currently stored in the database.
    """
    books = db.query(models.Book).all()
    return books


@app.get("/books/search/", response_model=List[schemas.BookOut])
def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
) -> List[schemas.BookOut]:
    """
    Search books by title, author, and/or year using optional query parameters.
    """
    query = db.query(models.Book)

    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    if year is not None:
        query = query.filter(models.Book.year == year)

    return query.all()


@app.put("/books/{book_id}", response_model=schemas.BookOut)
def update_book(
    book_id: int,
    book_in: schemas.BookUpdate,
    db: Session = Depends(get_db)
) -> schemas.BookOut:
    """
    Update an existing book using partial update fields.
    """
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    update_data = book_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete a book by its ID.
    """
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    db.delete(book)
    db.commit()
    return None
