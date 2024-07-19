from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.responses import FileResponse

from src.database import get_session, transaction
from src.exeptions import RequestEntityTooLargeException
from src.auth.dependencies import get_current_user_from_token
from src.auth.models import User
from src.auth.services import UserService
from src.files_upload.dependencies import valid_filename
from src.files_upload.models import FileUpload
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
    session: FileUploadService = Depends(get_session),
    user: User = Depends(get_current_user_from_token),
):
    file_service = FileUploadService(session)
    user_service = UserService(session)

    if user.used_mb + file_service._bytes_to_megabytes(upload_file.size) <= 200:
        async with transaction(session):
            uploaded_file = await file_service.upload(
                upload_file, user.id, upload_file.content_type[6:]
            )
            await user_service.update_used_mb(user, uploaded_file.size_mb, "add")
            return uploaded_file
    else:
        raise RequestEntityTooLargeException(
            "The uploaded file exceeds the user's allocated storage limit."
        )


@files_upload_router.get(
    "/{file_id}", status_code=status.HTTP_200_OK, response_class=FileResponse
)
async def get_uploaded_file(file: FileUpload = Depends(valid_filename)):
    return file.file_path


@files_upload_router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file: FileUpload = Depends(valid_filename),
    session: FileUploadService = Depends(get_session),
    user: User = Depends(get_current_user_from_token),
):
    file_service = FileUploadService(session)
    user_service = UserService(session)

    async with transaction(session):
        await user_service.update_used_mb(user, file.size_mb, "subtract")
        await file_service.delete_from_database(file)
