import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.config import settings
from src.exeptions import DatabaseException

logger = logging.getLogger(__name__)

engine = create_async_engine(settings.db.URL.get_secret_value(), echo=True)
session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with session_maker() as session:
            yield session
    except OSError as e:
        logger.error(f"Database connection failed: {e}")
        raise DatabaseException
