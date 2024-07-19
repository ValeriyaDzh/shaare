import logging

from src.exeptions import AlreadyExistsException, NotFoundException
from src.repositories import BaseRepository
from src.auth.utils import Password
from src.auth.models import User
from src.auth.schemas import CreateUser

logger = logging.getLogger(__name__)


class UserService(BaseRepository):

    def __init__(self, session):
        super().__init__(model=User, session=session)

    async def create(self, data: CreateUser) -> User:

        if await self.get_by_login(data.login):
            raise AlreadyExistsException(detail="This login is already in use")

        data_dict = data.model_dump()
        password = data_dict.pop("password")
        data_dict["hashed_password"] = Password.hash(password)
        logger.debug(f"Prepared user: {data_dict}")

        created_user = await self.save(data_dict)
        await self.session.commit()

        return created_user

    async def get_by_login(self, login: str) -> User | None:
        """
        Get user from the database.

        :param login: the user's login.
        :return: the User if found, else None.
        """

        user = await self.get("login", login)
        return user

    async def update_used_mb(self, current_user: User, mb: float, action: str) -> User:
        """
        Update `used_mb` for user in the database.

        :param current_user: the current user.
        :param mb: a megabytes to add or subtract from `used_mb`.
        :param action: `add` to add, `subtract` subtract from `used_mb` a megabytes.
        :return: the updated User.
        """
        new_used_mb = current_user.used_mb
        if action == "add":
            new_used_mb += mb
        elif action == "subtract":
            new_used_mb -= mb

        logger.debug(f"Megabytes to {action}: {new_used_mb}")
        updated_user = await self.update(
            "id", current_user.id, {"used_mb": new_used_mb}
        )

        return updated_user
