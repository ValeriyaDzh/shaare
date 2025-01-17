import aiofiles
import os
import logging
from pathlib import Path
from typing import BinaryIO
from uuid import UUID

logger = logging.getLogger(__name__)


class File:
    """
    Utility class for handling files operations.
    """

    @classmethod
    async def create_path(cls, filename: UUID, format: str) -> str:
        return f"{os.getcwd()}/src/uploaded_files/{filename}.{format}"

    @classmethod
    async def save_to_server(cls, path: str, data: BinaryIO) -> str:
        try:
            async with aiofiles.open(path, "+wb") as p:
                await p.write(data.read())
            if os.path.exists(path):
                return path

        except Exception as e:
            logger.error(f"Error saving the file on the server: {e}")

    @classmethod
    async def delete_from_server(cls, path: str) -> bool:
        try:
            os.remove(path)
            return os.path.exists(path) == False

        except FileNotFoundError as e:
            logger.debug(f"File {Path(path).name} not found: {e}")
            return False
