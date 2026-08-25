"""
FastAPI router exposing the URL shortening API.
"""

from fastapi import APIRouter, HTTPException, Depends, status, Response
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from storage import get_db
from shortener import ShortenerService
from config import settings

router = APIRouter()

class ShortenRequest(BaseModel):
    target_url: HttpUrl

class ShortenResponse(BaseModel):
    short_url: HttpUrl

@router.post("/shorten", response_model=ShortenResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(
    payload: ShortenRequest,
    db: Session = Depends(get_db)
):
    service = ShortenerService(db)
    try:
        code = service.shorten(str(payload.target_url))
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))

    short_url = f"{settings.BASE_URL.rstrip('/')}/{code}"
    return ShortenResponse(short_url=short_url)

@router.get("/{code}")
def redirect_to_target(
    code: str,
    db: Session = Depends(get_db)
):
    service = ShortenerService(db)
    try:
        target = service.resolve(code)
    except KeyError:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return Response(status_code=302, headers={"Location": target})

@router.get("/health")
def health_check():
    return {"status": "ok"}