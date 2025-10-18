from fastapi import FastAPI

__all__ = ["app"]

app = FastAPI(
    title="Card Trading Service", 
    version="0.1.0",
    debug=True,
)