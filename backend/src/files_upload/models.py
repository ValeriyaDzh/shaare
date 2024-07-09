from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base
from users.models import User


class FileUpload(Base):

    __tabelname__ = "file_upload"

    id = Column(Integer, primary_key=True)
    filename = Column(String, unique=True, nullable=False)
    size_mb = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(
        UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User", back_populates="files")
