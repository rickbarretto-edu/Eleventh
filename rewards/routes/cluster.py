from fastapi import APIRouter

router = APIRouter()

@router.get("/cluster/leader")
async def get_leader():
    pass
    
@router.post("/cluster/add")
async def add_peer():
    pass
    
@router.post("/cluster/health")
async def get_health():
    pass
