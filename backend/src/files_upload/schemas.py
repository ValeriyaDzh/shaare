from pydantic import BaseModel


class ShowAploadedFile(BaseModel):

    filename: str
    size_mb: float
