from fastapi import APIRouter

from vec2.user.endpoints import router as user_router

router = APIRouter(prefix="/v1")

# /users
router.include_router(user_router)
