import logging

from aiohttp import ClientSession, ClientResponseError
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.dao.complaint import ComplaintDao
from core.enums.complaint import SentimentEnum
from core.schemas.complaint import (
    ComplaintInSchema,
    ComplaintReadSchema,
    ComplaintCreateSchema,
)

log = logging.getLogger(__name__)


async def create_new_complaint(
    complaint: ComplaintInSchema,
    session: AsyncSession,
    client_session: ClientSession,
) -> ComplaintReadSchema:
    sentiment = SentimentEnum.unknown
    try:
        async with client_session.post(
            settings.resources.sentinel.url,
            data=complaint.text,
            raise_for_status=True,
        ) as response:
            json = await response.json()
            sentiment = json["sentiment"]
    except ClientResponseError as e:
        log.exception(
            "Ошибочный ответ от %s со статус кодом %s",
            settings.resources.sentinel.url,
            e.status,
        )
    except TimeoutError as e:
        log.exception(
            "Время ожидания ответа от %s истекло: %s",
            settings.resources.sentinel.url,
            e,
        )
    model = ComplaintCreateSchema(
        text=complaint.text,
        sentiment=sentiment,
        category="Другое",
    )
    record = await ComplaintDao(session=session).add(
        model,
    )
    return ComplaintReadSchema.model_validate(record, from_attributes=True)
