from fastapi import APIRouter


pages = APIRouter()

@pages.get("/")
async def homepage():
    return {"message": "Welcome to the Deck Management Service!"}

@pages.get("/{user}/deck")
async def user_page(user: str):
    return {"user": user, "deck": []}
