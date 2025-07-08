import logging

from core.models import Base
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

logger = logging.getLogger(__name__)


class BaseDAO[M: Base]:
    model: type[M] | None = None

    def __init__(self, session: AsyncSession):
        self._session = session
        if self.model is None:
            raise ValueError("Модель должна быть указана в дочернем классе")

    async def find_one_or_none_by_id(self, data_id: int) -> M | None:
        try:
            query = select(self.model).filter_by(id=data_id)
            result = await self._session.execute(query)
            record = result.scalar_one_or_none()
            logger.info(
                "Запись %s с ID %s %s.",
                self.model.__name__,
                data_id,
                "найдена" if record else "не найдена",
            )
            return record
        except SQLAlchemyError as e:
            logger.error("Ошибка при поиске записи с ID %s: %s", data_id, e)
            raise

    async def find_one_or_none(self, filters: BaseModel) -> M | None:
        filter_dict = filters.model_dump(exclude_unset=True)
        logger.info(
            "Поиск одной записи %s по фильтрам: %s",
            self.model.__name__,
            filter_dict,
        )
        try:
            query = select(self.model).filter_by(**filter_dict)
            result = await self._session.execute(query)
            record = result.scalar_one_or_none()
            logger.info(
                "Запись %s по фильтрам: %s",
                "найдена" if record else "не найдена",
                filter_dict,
            )
            return record
        except SQLAlchemyError as e:
            logger.error(
                "Ошибка при поиске записи по фильтрам %s: %s",
                filter_dict,
                e,
            )
            raise

    async def find_all(
        self,
        filters: BaseModel | None = None,
        sort_fields: list[str] | None = None,
    ) -> list[M]:
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        logger.info(
            "Поиск всех записей %s по фильтрам: %s",
            self.model.__name__,
            filter_dict,
        )
        try:
            query = select(self.model).filter_by(**filter_dict)
            if sort_fields:
                query = query.order_by(
                    *self._get_sorting_attrs(sort_fields=sort_fields)
                )
            result = await self._session.execute(query)
            records = result.scalars().all()
            logger.info("Найдено %s записей.", len(records))
            return records
        except SQLAlchemyError as e:
            logger.error(
                "Ошибка при поиске всех записей по фильтрам %s: %s",
                filter_dict,
                e,
            )
            raise

    async def add(self, values: BaseModel) -> M:
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(
            "Добавление записи %s с параметрами: %s",
            self.model.__name__,
            values_dict,
        )
        try:
            new_instance = self.model(**values_dict)
            self._session.add(new_instance)
            await self._session.flush()
            logger.info("Запись %s успешно добавлена.", self.model.__name__)
            return new_instance
        except SQLAlchemyError as e:
            await self._session.rollback()
            logger.error("Ошибка при добавлении записи %s", e)
