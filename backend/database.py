import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Get database URL from environment or use default
# Use absolute path for Windows compatibility
DATABASE_PATH = os.path.abspath("testbook.db")
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_PATH}")

# Normalize Postgres driver to psycopg (v3) if not explicitly set
if SQLALCHEMY_DATABASE_URL.startswith("postgresql://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

# SQLite-specific connection args (only needed for SQLite)
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# models.py uses the classic Column()/relationship() declarative style,
# not SQLAlchemy 2.0's Mapped[] annotated style. Relationship attributes
# there carry plain type annotations (e.g. `posts: List["Post"] = relationship(...)`)
# purely so mypy's SQLAlchemy plugin can type them - without this flag,
# SQLAlchemy's runtime mapper mistakes those for an incomplete attempt at
# the new Mapped[] style and raises MappedAnnotationError on startup.
Base.__allow_unmapped__ = True


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
