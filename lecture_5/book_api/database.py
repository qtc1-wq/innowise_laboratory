"""
database.py

Handles database connection.
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./books.db"

# SQLite engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency providing a database session.
    Closes the session after request completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
