"""
Integration tests for the ShortenerService using a temporary SQLite DB.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from storage import Base, init_db, get_db
from shortener import ShortenerService

SQLITE_MEMORY_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for each test."""
    engine = create_engine(SQLITE_MEMORY_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def test_shorten_and_resolve_success(db_session):
    service = ShortenerService(db_session, code_length=8)
    url = "https://www.example.com/some/long/path"

    # Shorten
    code = service.shorten(url)
    assert isinstance(code, str) and len(code) == 8

    # Resolve
    resolved = service.resolve(code)
    assert resolved == url

def test_shorten_invalid_url(db_session):
    service = ShortenerService(db_session)
    with pytest.raises(ValueError):
        service.shorten("not-a-valid-url")

def test_resolve_unknown_code(db_session):
    service = ShortenerService(db_session)
    with pytest.raises(KeyError):
        service.resolve("nonexistent")