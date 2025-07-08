from pydantic import BaseModel

from core.enums.complaint import StatusEnum, SentimentEnum


class ComplaintCreateSchema(BaseModel):
    text: str


class ComplaintReadSchema(BaseModel):
    id: int
    status: StatusEnum
    sentiment: SentimentEnum
