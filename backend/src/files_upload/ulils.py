import shutil
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
    async def save_to_server(cls, filename: UUID, data: BinaryIO, format: str) -> str:
        try:
            path = f"{os.getcwd()}/src/uploaded_files/{filename}.{format}"
            with open(path, "+wb") as p:
                shutil.copyfileobj(data, p)

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
