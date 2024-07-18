import logging
from uuid import UUID, uuid4
from fastapi import UploadFile

from src.exeptions import BadRequestException, AlreadyExists
from src.repositories import BaseRepository
from src.files_upload.models import FileUpload
from src.files_upload.ulils import File

logger = logging.getLogger(__name__)


class FileUploadService(BaseRepository):

    def __init__(self, session):
        super().__init__(model=FileUpload, session=session)

    async def get_file_by_id(self, file_id: UUID) -> FileUpload:
        file = await self.get("id", file_id)
        return file

    async def is_filename_exist(self, file_name: str) -> bool:
        file = await self.get("filename", file_name)
        return file is not None

    async def upload(self, data: UploadFile, user_id: UUID, format: str) -> FileUpload:
        if data.content_type[:5] == "image":
            if self.is_filename_exist(data.filename):
                raise AlreadyExists("File with this name already exist")

            file_id = uuid4()
            path = await File.create_path(file_id, format)
            try:
                uploaded_file = await self.add_to_database(
                    user_id, file_id, data.filename, path, data.size
                )
                await File.save_to_server(path, data.file)
                return uploaded_file

            except Exception as e:
                logger.error(f"Error saving the file in database: {e}")

        else:
            raise BadRequestException(
                "Invalid format. Valid file formats: PNG, JPEG, GIF, RAW, TIFF, BMP, PSD, SVG, PDF, EPS, AI, CDR"
            )

    async def add_to_database(
        self,
        user_id: UUID,
        file_id: UUID,
        filename: str,
        file_path: str,
        size_bytes: int,
    ) -> FileUpload:

        size_mb = self._bytes_to_megabytes(size_bytes)
        file_dict = {
            "id": file_id,
            "filename": filename,
            "user_id": user_id,
            "file_path": file_path,
            "size_mb": size_mb,
        }
        uploaded_file = await self.save(file_dict)

        return uploaded_file

    async def delete_from_database(self, file: FileUpload) -> None:

        if await File.delete_from_server(file.file_path):
            await self.delete(file.id)

    @staticmethod
    def _bytes_to_megabytes(bytes: int) -> float:
        return round(bytes / 1048576, 2)
