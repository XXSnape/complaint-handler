from datetime import datetime

from core.enums.complaint import (
    CategoryLiteral,
    SentimentEnum,
    StatusEnum,
)
from pydantic import BaseModel


class ComplaintInSchema(BaseModel):
    """
    Схема для создания жалобы.
    """
    text: str


class ComplaintCreateSchema(ComplaintInSchema):
    """
    Схема для создания жалобы с дополнительными полями.
    """
    sentiment: SentimentEnum | None = None
    category: CategoryLiteral | None = None


class ComplaintReadSchema(ComplaintCreateSchema):
    """
    Схема для чтения информации о жалобе.
    """
    id: int
    status: StatusEnum


class ComplaintAllInfoSchema(ComplaintReadSchema):
    """
    Схема для получения полной информации о жалобе.
    """
    timestamp: datetime


class OpenComplaintsSchema(BaseModel):
    """
    Схема для списка открытых жалоб, созданных в течение последнего часа.
    """
    complaints: list[ComplaintAllInfoSchema]
