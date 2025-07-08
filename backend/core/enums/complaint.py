from enum import StrEnum
from typing import Literal


class StatusEnum(StrEnum):
    open = "open"
    closed = "closed"


class SentimentEnum(StrEnum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"
    unknown = "unknown"


CategoryLiteral = Literal["Техническая", "Оплата", "Другое"]
