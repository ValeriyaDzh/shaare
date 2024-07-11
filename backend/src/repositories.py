import logging
from typing import Any
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.exeptions import DatabaseException

logger = logging.getLogger(__name__)


class BaseRepository:
    """
    Base repository providing generic database
    Create, Get, Update operations.
    """

    def __init__(self, model, session: AsyncSession):
        self.model = model
        self.session = session

    async def save(self, playload: dict[str, Any]) -> Any:
        """
        Save a new entity in the database.

        :param payload: data for the new entity.
        :return: the saved entity.
        :raises DatabaseException: if a database error occurs.
        """
        try:
            entity = self.model(**playload)
            self.session.add(entity)
            await self.session.commit()
            return entity

        except SQLAlchemyError as e:
            logger.error(f"Error save entity in the database: {e}")
            raise DatabaseException

    async def get(self, key: str, value: str) -> Any:
        """
        Get entities from the database by a specified field.

        :param key: field name.
        :param value: field value.
        :return: the entity if found, else None.
        :raises DatabaseException: if a database error occurs.
        """
        try:
            entity = await self.session.execute(
                select(self.model).where((getattr(self.model, key) == value))
            )
            return entity.scalar_one_or_none()

        except SQLAlchemyError as e:
            logger.error(f"Error get entity from the database: {e}")
            raise DatabaseException

    async def update(self, key: str, value: str, playload: dict[str, Any]) -> Any:
        """
        Update an entity in the database.

        :param key: field name to search for the entity.
        :param value: field value to search for the entity.
        :param payload: data for updating the entity.
        :return: the updated entity.
        :raises DatabaseException: If a database error occurs.
        """
        try:
            updated_entity = (
                update(self.model)
                .where(getattr(self.model, key) == value)
                .values(**playload)
                .returning(self.model)
            )
            entity = await self.session.execute(updated_entity)
            await self.session.commit()
            return entity.scalar_one()

        except SQLAlchemyError as e:
            logger.error(f"Error update entity in the database: {e}")
            raise DatabaseException
