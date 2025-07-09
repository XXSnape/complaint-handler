from core.config import settings
from fastapi import APIRouter

from .complaints import router as complaints_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(
    complaints_router,
    prefix=settings.api.v1.complaints,
)
