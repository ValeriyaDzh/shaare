import shutil
from fastapi import APIRouter, Depends, status, UploadFile, File

from src.auth.dependencies import get_current_user_from_token
from src.auth.models import User
from src.files_upload.dependencies import get_uploadfile_service
from src.files_upload.schemas import ShowAploadedFile
from src.files_upload.services import FileUploadService


files_upload_router = APIRouter(prefix="", tags=["Files_Upload"])


@files_upload_router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowAploadedFile,
    # responses={status.HTTP_401_UNAUTHORIZED},
)
async def upload_file(
    upload_file: UploadFile = File(...),
    file_service: FileUploadService = Depends(get_uploadfile_service),
    user: User = Depends(get_current_user_from_token),
):
    uploaded_file = await file_service.upload(upload_file, user.id)

    return uploaded_file
