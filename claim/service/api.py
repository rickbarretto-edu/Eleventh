from fastapi import APIRouter

service = APIRouter(
    prefix="/api",
)

@service.get("/claim")
async def claim(n: int):
    cards = [{"id": i, "name": f"Card {i}", "power": i * 5} for i in range(1, n + 1)]
    return {"status": "success", "cards": cards}


@service.post("/store")
async def store(cards: list[dict]):
    # Here you would normally store the cards in a database or similar
    return {"status": "success", "stored_cards": cards}
