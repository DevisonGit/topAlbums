from pydantic import BaseModel


class Album(BaseModel):
    id: int
    name: str
    artist: str
    label: str
    year: int
    rating: float | None = None
