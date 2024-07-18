from uuid import UUID
from pydantic import BaseModel


class ShowAploadedFile(BaseModel):

    id: UUID
    filename: str
    size_mb: float
