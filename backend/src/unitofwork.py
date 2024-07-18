from src.database import async_session_maker
from src.auth.services import UserService
from src.files_upload.services import FileUploadService


class UnitOfWork:

    def __init__(self):
        self._session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self._session_factory()
        self.user_service = UserService(self.session)
        self.file_service = FileUploadService(self.session)

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
