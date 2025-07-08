from enum import StrEnum


class StatusEnum(StrEnum):
    open = "open"
    closed = "closed"


class SentimentEnum(StrEnum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"
    unknown = "unknown"
