from fastapi import FastAPI

from decks.service.api import service
from decks.service.web import pages

__all__ = ["app"]

app = FastAPI(
    title="Deck Management Service", 
    version="0.1.0",
    debug=True,
)

app.include_router(service)
app.include_router(pages)