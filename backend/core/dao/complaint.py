import logging
from datetime import datetime, timedelta
from typing import Sequence

from core.enums.complaint import StatusEnum
from core.models import Complaint
from fastapi import HTTPException, status
from sqlalchemy import select, update

from .base import BaseDAO

logger = logging.getLogger(__name__)


class ComplaintDao(BaseDAO[Complaint]):
    """
    DAO для работы с жалобами в базе данных.
    """

    model = Complaint

    async def get_complaints_in_last_hour(
        self,
    ) -> Sequence[Complaint]:
        """
        Получает список открытых жалоб, созданных в течение последнего часа,
        """
        hour_ago = datetime.now() - timedelta(hours=1)
        query = select(self.model).where(
            self.model.timestamp >= hour_ago,
            self.model.status == StatusEnum.open,
            self.model.category != "Другое",
        )
        result = await self._session.execute(query)
        return result.scalars().all()

    async def close_complaint(
        self,
        complaint_id: int,
    ) -> None:
        """
        Закрывает жалобу по ID, устанавливая статус "closed".
        """
        logger.info("Закрытие жалобы с ID %s", complaint_id)
        query = (
            update(self.model)
            .where(self.model.id == complaint_id)
            .values(status="closed")
        )
        result = await self._session.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        logger.info("Жалоба с ID %s успешно закрыта", complaint_id)
