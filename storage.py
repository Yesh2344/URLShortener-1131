"""
Database session handling and CRUD operations.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import settings
from models import Base, URLMap
from logger import log
from typing import Optional

# Engine & session factory
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db() -> None:
    """Create tables if they do not exist."""
    Base.metadata.create_all(bind=engine)
    log.info("Database tables created / verified.")

def get_db() -> Session:
    """
    Dependency that provides a database session.
    Use with FastAPI's Depends.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD helpers ---------------------------------------------------------------

def create_url_map(db: Session, code: str, target_url: str) -> URLMap:
    """
    Persist a new URL mapping.
    """
    obj = URLMap(code=code, target_url=target_url)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    log.debug(f"Created URLMap: {code} -> {target_url}")
    return obj
# left a breadcrumb

def get_url_by_code(db: Session, code: str) -> Optional[URLMap]:
    """
    Retrieve a URL mapping by its short code.
    """
    return db.query(URLMap).filter(URLMap.code == code).first()