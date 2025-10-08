"""Web UI pages for Deck management."""

from pathlib import Path
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated

from eleventh.decks.repo import InMemoryDecks


route = APIRouter(
    tags=["decks", "ui"],
)


def get_decks() -> InMemoryDecks:
    """Provide the Decks repository instance."""
    return InMemoryDecks()


# Setup templates directory
templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent / "static"
)


@route.get("/", response_class=HTMLResponse)
async def deck_manager_ui(request: Request):
    """Serve the deck management web UI."""
    return templates.TemplateResponse("deck_manager.html", {"request": request})


@route.get("/user/{user_id}", response_class=HTMLResponse)
async def user_deck_ui(
    request: Request, 
    user_id: str,
    decks: Annotated[InMemoryDecks, Depends(get_decks)]
):
    """Serve the user-specific deck management UI."""
    return templates.TemplateResponse(
        "deck_manager.html", 
        {
            "request": request,
            "user_id": user_id
        }
    )
