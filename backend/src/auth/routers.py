from fastapi import APIRouter, Depends, status
from src.auth.schemas import LoginForm, Token
from src.auth.dependencies import get_user_service
from src.auth.schemas import ShowUser, CreateUser, UserAlreadyExistException
from src.auth.services import UserService

users_auth_router = APIRouter(prefix="/auth", tags=["Auth"])
users_router = APIRouter(prefix="/auth", tags=["User"])


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
    pass
