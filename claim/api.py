from fastapi import FastAPI

from claim.service.api import service
from claim.service.web import pages


__all__ = ["app"]


app = FastAPI(
    title="Rewarding Claim Service", 
    version="0.1.0",
    debug=True,
)

app.include_router(service)
app.include_router(pages)