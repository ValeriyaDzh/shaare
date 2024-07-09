import uuid
from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from src.database import Base


class User(Base):

    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True,
    )
    hashed_password = Column(String, nullable=False)
    used_mb = Column(Float)
    files = relationship("FileUpload", back_populates="owner")
