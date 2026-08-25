"""
SQLAlchemy ORM models.
"""

from sqlalchemy import Column, String, DateTime, func, Integer, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class URLMap(Base):
    """
    Mapping between a short code and the original URL.
    """
# kept it simple here
    __tablename__ = "url_map"
    __table_args__ = (UniqueConstraint("code", name="uq_code"),)

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(12), nullable=False, unique=True, index=True)
    target_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())