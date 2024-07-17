import logging
import shutil
import os
from pathlib import Path
from uuid import UUID
from typing import BinaryIO
from fastapi import UploadFile
from src.repositories import BaseRepository
from src.files_upload.models import FileUpload

logger = logging.getLogger(__name__)


class FileUploadService(BaseRepository):

    def __init__(self, session, model=FileUpload):
        super().__init__(model=model, session=session)

    async def get_file_by_name(self, filename: str) -> FileUpload:
        file = await self.get("filename", filename)
        return file

    async def upload(self, data: UploadFile, user_id: UUID) -> FileUpload:
        path = await self._save_to_server(data.filename, data.file)

        if path:
            uploaded_file = await self.add_to_database(
                user_id, data.filename, path, data.size
            )
            return uploaded_file

    @staticmethod
    async def _save_to_server(filename: str, data: BinaryIO) -> str:
        try:
            path = f"{Path(os.getcwd())}/src/uploaded_files/{filename}"
            with open(path, "+wb") as p:
                shutil.copyfileobj(data, p)

            if os.path.exists(path):
                return path

        except Exception as e:
            logger.error(f"Error saving the file on the server: {e}")

    async def add_to_database(
        self, user_id: UUID, filename: str, file_path: str, size_bytes: int
    ) -> FileUpload:

        size_mb = self._bytes_to_megabytes(size_bytes)
        file_dict = {
            "filename": filename,
            "user_id": user_id,
            "file_path": file_path,
            "size_mb": size_mb,
        }
        uploaded_file = await self.save(file_dict)

        return uploaded_file

    @staticmethod
    def _bytes_to_megabytes(bytes: int) -> float:
        return round(bytes / 1048576, 2)
