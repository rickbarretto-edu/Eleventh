
from fastapi import APIRouter


router = APIRouter()

@router.get("/")
async def homepage():
    return {"message": "Welcome to the Claim Service API"}

@router.get("/admin")
async def admin_panel():
    return {"message": "Admin Panel - Manage your cluster here"}

@router.get("/admin/logs")
async def admin_logs():
    return {"message": "Admin Logs - View your logs here"}

@router.post("/admin/cards")
async def add_card(card: dict):
    return {"status": "success", "added_card": card}
