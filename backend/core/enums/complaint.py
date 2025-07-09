from enum import StrEnum
from typing import Literal


class StatusEnum(StrEnum):
    """
    Enum для статуса жалобы.
    """

    open = "open"
    closed = "closed"


class SentimentEnum(StrEnum):
    """
    Enum для тональности жалобы.
    """

    positive = "positive"
    negative = "negative"
    neutral = "neutral"
    unknown = "unknown"


CategoryLiteral = Literal["Техническая", "Оплата", "Другое"]
