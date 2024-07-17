import logging
from uuid import UUID, uuid4
from fastapi import UploadFile

from src.exeptions import BadRequestException
from src.repositories import BaseRepository
from src.files_upload.models import FileUpload
from src.files_upload.ulils import File

logger = logging.getLogger(__name__)


class FileUploadService(BaseRepository):

    def __init__(self, session, model=FileUpload):
        super().__init__(model=model, session=session)

    async def get_file_by_id(self, file_id: UUID) -> FileUpload:
        file = await self.get("id", file_id)
        return file

    async def upload(self, data: UploadFile, user_id: UUID, format: str) -> FileUpload:

        if data.content_type[:5] == "image":

            file_id = uuid4()
            path = await File.save_to_server(file_id, data.file, format)

            if path:
                uploaded_file = await self.add_to_database(
                    user_id, file_id, data.filename, path, data.size
                )
                return uploaded_file

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
