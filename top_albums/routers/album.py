from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from top_albums.databases.database import get_session
from top_albums.models.album import Album
from top_albums.schemas.album import AlbumList, AlbumPublic
from top_albums.services.filter_service import build_filter

router = APIRouter(prefix='/albums', tags=['album'])
Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AlbumPublic)
def create_album(album: AlbumPublic, session: Session):
    db_album = session.scalar(select(Album).where(Album.id == album.id))
    if db_album:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Album already exists'
        )
    db_album = Album(**album.model_dump())
    session.add(db_album)
    session.commit()
    session.refresh(db_album)

    return db_album


@router.get('/', response_model=AlbumList)
def list_albums(  # noqa
    session: Session,
    name: str = Query(None),
    artist: str = Query(None),
    label: str = Query(None),
    year: int = Query(None),
    rating: float = Query(None),
):
    filters = build_filter(name, artist, label, year, rating)

    if not filters:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='At least one filter parameter must be provided.',
        )

    query = select(Album).where(and_(*filters))
    albums = session.scalars(query).all()

    return {'Albums': albums}
