from fastapi import FastAPI

__all__ = ["app"]

app = FastAPI(
    title="Deck Management Service", 
    version="0.1.0",
    debug=True,
)
