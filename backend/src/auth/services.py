import logging

from src.exeptions import AlreadyExists, NotFoundException
from src.repositories import BaseRepository
from src.auth.utils import Password
from backend.src.auth.models import User
from src.auth.schemas import CreateUser

logger = logging.getLogger(__name__)


class UserService(BaseRepository):

    def __init__(self, session, model=User):
        super.__init__(session, model=model)

    async def create(self, data: CreateUser) -> User:

        if self.get("login", data.login):
            raise AlreadyExists(detail="This login is already in use")

        data_dict = data.model_dump()
        password = data_dict.pop("password")
        data_dict["hashed_password"] = Password.hash(password)
        logger.debug(f"Prepared user: {data_dict}")

        created_user = await self.save(data_dict)

        return created_user

    async def get_by_login(self, login: str) -> User | None:
        """
        Get user from the database.

        :param login: the user's login.
        :param mb: a megabytes to add to `used_mb`.
        :return: the User.
        :raises NotFoundException: If the user whith this login doesn't exist.
        """

        user = self.get("login", login)
        if not user:
            raise NotFoundException(detail="User not found")

        return await self.get("login", login)

    async def add_mb(self, current_user: User, mb: float) -> User:
        """
        Update `used_mb` for user in the database.

        :param current_user: the current user.
        :param mb: a megabytes to add to `used_mb`.
        :return: the updated User.
        """
        new_used_mb = current_user.used_mb + mb
        logger.debug(f"Megabytes to add: {new_used_mb}")
        updated_user = await self.update(
            "id", current_user.id, {"used_mb": new_used_mb}
        )

        return updated_user
