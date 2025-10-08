"""Deck management microservice.

Usage
-----

        uvicorn eleventh.decks.app:app --reload --host --port 8000
"""


from fastapi import FastAPI

from eleventh.decks.web import api
from eleventh.decks.web import pages

app = FastAPI()
app.include_router(pages.route)
app.include_router(api.route)

