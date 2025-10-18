from fastapi import FastAPI

from rewards.service.api import service
from rewards.service.web import pages

__all__ = ["app"]

app = FastAPI(
    title="Rewarding Generation Service", 
    version="0.1.0",
    debug=True,
)

app.include_router(service)
app.include_router(pages)