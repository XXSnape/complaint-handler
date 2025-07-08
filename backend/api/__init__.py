from fastapi import APIRouter

from core.config import settings
from .v1 import router as complaint_api_v1

router = APIRouter(
    prefix=settings.api.prefix,
)
router.include_router(complaint_api_v1)
