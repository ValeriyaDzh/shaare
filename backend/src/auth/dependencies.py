import logging
from jose import JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.exeptions import InvalidCredentialsException
from src.auth.utils import JWTToken
from src.auth.models import User
from src.auth.services import UserService

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/sign-in")


async def get_user_service(session: AsyncSession = Depends(get_session)):
    return UserService(session=session)


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
) -> User:
    """
    Retrieve the current user by the provided JWT token.

    This function decodes the JWT token to extract the user's login information
    and retrieves information about the corresponding user from the database.

    If the token is invalid or if the user doesn't exist,
    InvalidCredentials exception is raised.
    """
    try:
        playload = JWTToken.decode(token)
        login: str = playload.get("sub")
        if login is None:
            raise InvalidCredentialsException
    except JWTError as e:
        logger.error(f"Error decoding jwt token: {e}")
        raise InvalidCredentialsException

    user = await user_service.get_by_login(login=login)
    if user is None:
        raise InvalidCredentialsException
    return user
