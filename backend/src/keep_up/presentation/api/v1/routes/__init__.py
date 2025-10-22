from fastapi import APIRouter

from .users import router as users_router
from .domains import router as domains_router

router = APIRouter(prefix="/v1", tags=["v1"])
router.include_router(users_router)
router.include_router(domains_router)

__all__ = ("router",)
