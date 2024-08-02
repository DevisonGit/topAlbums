from pydantic import BaseModel


class AlbumPublic(BaseModel):
    id: int
    name: str
    artist: str
    label: str
    year: int
    rating: float | None = None


class AlbumList(BaseModel):
    Albums: list[AlbumPublic]


class AlbumUpdate(BaseModel):
    rating: float | None = None
