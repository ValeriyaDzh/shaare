from fastapi import HTTPException, status


class DatabaseException(HTTPException):

    def __init__(self, detail: str = "Server error"):
        super.__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class NotFoundException(HTTPException):

    def __init__(self, detail: str = "Not found") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class AlreadyExists(HTTPException):

    def __init__(self, detail: str = "Already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InvalidCredentialsException(HTTPException):

    def __init__(self, detail: str = "Could not validate credentials") -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
