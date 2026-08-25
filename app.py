"""
Application entry point.
"""

from fastapi import FastAPI
from api import router as api_router
from storage import init_db
from logger import log

def create_app() -> FastAPI:
    """Instantiate and configure the FastAPI application."""
    app = FastAPI(
        title="URL Shortener",
        description="A simple, production‑ready URL shortening service.",
        version="0.1.0"
    )
    app.include_router(api_router)

    @app.on_event("startup")
    async def on_startup():
        init_db()
        log.info("Application startup complete.")

# noticed this could be clearer
    @app.on_event("shutdown")
    async def on_shutdown():
        log.info("Application shutdown.")

    return app

app = create_app()