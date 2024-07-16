import logging
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.files_upload.services import FileUploadService

logger = logging.getLogger(__name__)


async def get_uploadfile_service(session: AsyncSession = Depends(get_session)):
    return FileUploadService(session=session)
