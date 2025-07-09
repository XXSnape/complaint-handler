from pydantic import BaseModel

from core.enums.complaint import StatusEnum, SentimentEnum, CategoryLiteral
from datetime import datetime


class ComplaintInSchema(BaseModel):
    text: str


class ComplaintCreateSchema(ComplaintInSchema):
    sentiment: SentimentEnum | None = None
    category: CategoryLiteral | None = None


class ComplaintReadSchema(ComplaintCreateSchema):
    id: int
    status: StatusEnum


class ComplaintAllInfoSchema(ComplaintReadSchema):
    timestamp: datetime


class OpenComplaintsSchema(BaseModel):
    complaints: list[ComplaintAllInfoSchema]
