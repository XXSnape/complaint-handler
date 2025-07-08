from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.complaint import ComplaintCreateSchema, ComplaintReadSchema

router = APIRouter(tags=["Complaints"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ComplaintReadSchema,
)
async def create_complaint(
    complaint: ComplaintCreateSchema,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
):
    pass
