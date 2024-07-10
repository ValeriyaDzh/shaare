from pydantic import BaseModel


class CreateUser(BaseModel):

    login: str
    password: str


class ShowUser(BaseModel):

    login: str
    used_mb: float | None = None


class UpdateUser(BaseModel):

    used_mb: float | None = None


class LoginForm(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserAlreadyExistException:

    code: int
    detail: str


# class UserNotFoundException:

#     code: 404
#     detail: str = "User doesn't found"
