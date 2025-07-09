from datetime import datetime

from core.enums.complaint import (
    CategoryLiteral,
    SentimentEnum,
    StatusEnum,
)
from sqlalchemy import TEXT, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Complaint(Base):
    """
    Модель для хранения информации о жалобах пользователей.
    """

    text: Mapped[str] = mapped_column(TEXT)
    status: Mapped[StatusEnum] = mapped_column(
        default=StatusEnum.open, server_default=StatusEnum.open
    )
    timestamp: Mapped[datetime] = mapped_column(
        default=datetime.now,
        server_default=func.now(),
    )
    sentiment: Mapped[SentimentEnum]
    category: Mapped[CategoryLiteral]
