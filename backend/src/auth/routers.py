from fastapi import APIRouter, Depends, status

from src.exeptions import InvalidCredentialsException
from src.auth.schemas import LoginForm, Token
from src.auth.dependencies import get_user_service
from src.auth.schemas import ShowUser, CreateUser, UserAlreadyExistException
from src.auth.services import UserService
from src.auth.utils import Password, JWTToken

users_auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@users_auth_router.post(
    "/sign-up",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowUser,
    responses={status.HTTP_409_CONFLICT: {"model": UserAlreadyExistException}},
)
async def create_user(
    user_data: CreateUser, user_service: UserService = Depends(get_user_service)
):
    return await user_service.create(user_data)


@users_auth_router.post(
    "/sign-in", status_code=status.HTTP_200_OK, response_model=Token
)
async def login_for_access_token(
    form_data: LoginForm, user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_by_login(form_data.login)

    if user and Password.verify(form_data.password, user.hashed_password):
        access_token = JWTToken.create_access_token({"sub": form_data.login})
    else:
        raise InvalidCredentialsException("Incorrect login or password")

    return {"access_token": access_token, "token_type": "bearer"}
