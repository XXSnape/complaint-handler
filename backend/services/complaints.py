import asyncio
import logging

from aiohttp import ClientSession, ClientResponseError
from google import genai
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.dao.complaint import ComplaintDao
from core.enums.complaint import SentimentEnum, CategoryLiteral
from core.schemas.complaint import (
    ComplaintInSchema,
    ComplaintReadSchema,
    ComplaintCreateSchema,
)

log = logging.getLogger(__name__)


async def get_category(text: str) -> CategoryLiteral:
    client = genai.Client(api_key=settings.resources.google.key)
    try:
        result = (
            await client.aio.models.generate_content(
                model=settings.resources.google.model,
                contents=f"Определи категорию этой жалобы: {text}.\n\n"
                f'Варианты: "Техническая", "Оплата", "Другое". Дай ответ только одним словом.',
            )
        ).text.title()
        if result not in ["Техническая", "Оплата", "Другое"]:
            return "Другое"
        return result
    except Exception as e:
        log.exception("Ошибка при определении категории для: %s", text)
        return "Другое"


async def get_sentiment(
    text: str,
    client_session: ClientSession,
) -> SentimentEnum:
    try:
        async with client_session.post(
            settings.resources.sentinel.url,
            data=text,
            raise_for_status=True,
        ) as response:
            json = await response.json()
            return json["sentiment"]
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
    return SentimentEnum.unknown


async def create_new_complaint(
    complaint: ComplaintInSchema,
    session: AsyncSession,
    client_session: ClientSession,
) -> ComplaintReadSchema:

    sentiment, category = await asyncio.gather(
        get_sentiment(
            text=complaint.text,
            client_session=client_session,
        ),
        get_category(text=complaint.text),
    )

    model = ComplaintCreateSchema(
        text=complaint.text,
        sentiment=sentiment,
        category=category,
    )
    record = await ComplaintDao(session=session).add(
        model,
    )
    schema = ComplaintReadSchema.model_validate(record, from_attributes=True)
    if schema.category == "Другое":
        schema.category = None
    return schema
