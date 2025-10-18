from fastapi import APIRouter

service = APIRouter(
    prefix="/api"
)

@service.get("/reward")
async def generate(n: int):
    rewards = [{"id": i, "name": f"Reward {i}", "value": i * 10} for i in range(1, n + 1)]
    return {"status": "success", "rewards": rewards}