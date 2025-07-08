import logging
from typing import Annotated

from aiohttp import ClientSession
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies.client import get_client_session
from core.models import db_helper
from core.schemas.complaint import (
    ComplaintInSchema,
    ComplaintReadSchema,
)
from services.complaints import create_new_complaint

router = APIRouter(tags=["Complaints"])

log = logging.getLogger(__name__)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ComplaintReadSchema,
)
async def create_complaint(
    complaint: ComplaintInSchema,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
    client_session: Annotated[ClientSession, Depends(get_client_session)],
):
    return await create_new_complaint(
        complaint=complaint,
        session=session,
        client_session=client_session,
    )
