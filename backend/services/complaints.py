import asyncio
import logging

from aiohttp import ClientResponseError, ClientSession
from core.config import settings
from core.dao.complaint import ComplaintDao
from core.enums.complaint import CategoryLiteral, SentimentEnum
from core.schemas.complaint import (
    ComplaintCreateSchema,
    ComplaintInSchema,
    ComplaintReadSchema,
)
from huggingface_hub import AsyncInferenceClient
from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger(__name__)


async def get_category(
    text: str,
) -> CategoryLiteral:
    """
    Определяет категорию жалобы с помощью AI-модели.
    """
    client = AsyncInferenceClient(
        model=settings.resources.hf.model,
        token=settings.resources.hf.token,
    )
    try:
        response = await client.chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": f"Определи категорию этой жалобы: \n\n{text}\n\n"
                    f'Варианты: "Техническая", "Оплата", "Другое". '
                    f"Дай ответ только одним из этих слов.",
                }
            ],
        )
        content = response.choices[0].message.content.lower()
        # Бывают случаи, когда модель выдает ответ, который точно не
        # соответствует ожидаемым категориям
        if "техн" in content:
            return "Техническая"
        if "опл" in content:
            return "Оплата"
    except Exception:
        log.exception("Ошибка при определении категории для: %s", text)
    return "Другое"


async def get_sentiment(
    text: str,
    client_session: ClientSession,
) -> SentimentEnum:
    """
    Определяет тональность текста.
    """
    try:
        async with client_session.post(
            settings.resources.sentinel.url,
            data=text,
            raise_for_status=True,
        ) as response:
            json = await response.json()
            result = json["sentiment"]
            if result in SentimentEnum:
                return result
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
    """
    Создает новую жалобу, определяя ее тональность и категорию.
    """

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
    schema = ComplaintReadSchema.model_validate(
        record,
        from_attributes=True,
    )
    if schema.category == "Другое":
        schema.category = None
    return schema
