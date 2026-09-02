"""
Database connection and session management.
Provides engine, session factory, and dependency injection for FastAPI.
"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from loguru import logger

from config import settings
from data.schemas.models import Base

# ─────────────────────────────────────────────────────────────
# Engine — connection pool tuned for a dev environment
# ─────────────────────────────────────────────────────────────
engine = create_engine(
    settings.database_url,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,       # detect stale connections
    echo=settings.app_env == "development",
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ─────────────────────────────────────────────────────────────
# Table creation helper
# ─────────────────────────────────────────────────────────────
def init_db() -> None:
    """Create all tables if they don't exist."""
    logger.info("Initialising database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ready.")


def check_connection() -> bool:
    """Verify database connectivity. Returns True if successful."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.error(f"Database connection failed: {exc}")
        return False


# ─────────────────────────────────────────────────────────────
# Session context manager (for scripts)
# ─────────────────────────────────────────────────────────────
@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager that provides a transactional session."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ─────────────────────────────────────────────────────────────
# FastAPI dependency injection
# ─────────────────────────────────────────────────────────────
def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency: yields a DB session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
