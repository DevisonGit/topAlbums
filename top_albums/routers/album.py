from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from top_albums.databases.database import get_session
from top_albums.models.album import Album as AlbumModel
from top_albums.schemas.album import Album

router = APIRouter(prefix='/album', tags=['album'])
Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Album)
def create_album(album: Album, session: Session):
    db_album = session.scalar(
        select(AlbumModel).where(AlbumModel.id == album.id)
    )
    if db_album:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Album already exists'
        )
    db_album = AlbumModel(**album.model_dump())
    session.add(db_album)
    session.commit()
    session.refresh(db_album)

    return db_album
