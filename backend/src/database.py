from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("...", echo=True)
session_maker = sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


def get_session():
    try:
        with session_maker() as session:
            yield session
    except OSError as e:
        print(f"Failed to connect to the database: {e}")
