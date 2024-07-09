from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from .config import settings

engine = create_engine(settings.db.URL.get_secret_value(), echo=True)
session_maker = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_session():
    try:
        with session_maker() as session:
            yield session
    except OSError as e:
        print(f"Failed to connect to the database: {e}")
