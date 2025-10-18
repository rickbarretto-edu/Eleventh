from fastapi import FastAPI

from trade.service.api import service
from trade.service.web import pages

__all__ = ["app"]

app = FastAPI(
    title="Card Trading Service", 
    version="0.1.0",
    debug=True,
)

app.include_router(service)
app.include_router(pages)
