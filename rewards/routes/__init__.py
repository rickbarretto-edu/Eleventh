from fastapi import APIRouter

router = APIRouter()
router.include_router(api)
router.include_router(cluster)
