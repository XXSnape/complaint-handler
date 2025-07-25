import logging
from typing import Annotated

from aiohttp import ClientSession
from core.dao.complaint import ComplaintDao
from core.dependencies.clients import get_client_session
from core.models import db_helper
from core.schemas.complaint import (
    ComplaintAllInfoSchema,
    ComplaintInSchema,
    ComplaintReadSchema,
    OpenComplaintsSchema,
)
from core.schemas.ok import OkSchema
from fastapi import APIRouter, Depends, status
from services.complaints import create_new_complaint
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Complaints"])

log = logging.getLogger(__name__)


@router.get("")
async def get_complaints(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
):
    """
    Выводит список открытых жалоб, которые были созданы в течение последнего часа.
    """
    dao = ComplaintDao(session=session)
    complaints = await dao.get_complaints_in_last_hour()

    return OpenComplaintsSchema(
        complaints=[
            ComplaintAllInfoSchema.model_validate(complaint, from_attributes=True)
            for complaint in complaints
        ]
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ComplaintReadSchema,
    response_model_exclude_none=True,
)
async def create_complaint(
    complaint: ComplaintInSchema,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
    client_session: Annotated[
        ClientSession,
        Depends(get_client_session),
    ],
):
    """
    Создает новую жалобу.
    """
    return await create_new_complaint(
        complaint=complaint,
        session=session,
        client_session=client_session,
    )


@router.post(
    "/{complaint_id}",
    response_model=OkSchema,
)
async def change_status(
    complaint_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session),
    ],
):
    """
    Закрывает жалобу по ее ID.
    """
    dao = ComplaintDao(session=session)
    await dao.close_complaint(complaint_id=complaint_id)
    return OkSchema()
