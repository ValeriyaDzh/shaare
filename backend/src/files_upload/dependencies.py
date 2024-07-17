import logging
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.exeptions import NotFoundException
from src.files_upload.models import FileUpload
from src.files_upload.services import FileUploadService

logger = logging.getLogger(__name__)


async def get_uploadfile_service(session: AsyncSession = Depends(get_session)):
    return FileUploadService(session=session)


async def valid_filename(
    file_name: str, file_service: FileUploadService = Depends(get_uploadfile_service)
) -> FileUpload:

    file = await file_service.get_file_by_name(file_name)
    if file is None:
        raise NotFoundException(f"Not found file: {file_name}")
    return file
