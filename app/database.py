from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.models import Base

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "learning_platform.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

# Set SQL_ECHO=1 to print generated SQL statements.
SQL_ECHO = os.getenv("SQL_ECHO", "0") == "1"

engine = create_engine(
    DATABASE_URL,
    echo=SQL_ECHO,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
)


@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record) -> None:
    """Enable foreign-key constraints for every SQLite connection."""
    del connection_record
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_database() -> None:
    """Create all tables that do not exist."""
    Base.metadata.create_all(engine)


def reset_database() -> None:
    """Delete and recreate all tables for a clean demonstration."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
