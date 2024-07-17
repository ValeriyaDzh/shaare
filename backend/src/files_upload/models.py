from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database import Base
from src.auth.models import User


class FileUpload(Base):

    __tablename__ = "file_upload"

    id = Column(UUID, primary_key=True)
    filename = Column(String, unique=True, nullable=False)
    file_path = Column(String, nullable=False)
    size_mb = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(
        UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )

    # owner = relationship("User", back_populates="files")
