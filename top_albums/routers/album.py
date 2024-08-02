from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from top_albums.databases.database import get_session
from top_albums.models.album import Album
from top_albums.schemas.album import AlbumList, AlbumPublic
from top_albums.services.filter_service import build_filter

router = APIRouter(prefix='/albums', tags=['album'])
Session = Annotated[Session, Depends(get_session)]
templates = Jinja2Templates(directory='templates')


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
    request: Request,
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

    return templates.TemplateResponse(
        'album/list.html', {'request': request, 'albums': albums}
    )


@router.get('/search', response_class=HTMLResponse)
async def get_search_form(request: Request):
    return templates.TemplateResponse(
        'album/search.html', {'request': request}
    )


@router.get('/playing', response_model=AlbumList)
def get_playing_now(request: Request, session: Session):
    query = select(Album).where(Album.playing)
    albums = session.scalars(query).all()

    return templates.TemplateResponse(
        'album/playing.html', {'request': request, 'albums': albums}
    )


@router.post('/{album_id}', response_model=AlbumList)
def update_rating(
    request: Request,
    session: Session,
    album_id: int,
    rating: Optional[float] = Form(None),
):
    db_album = session.scalar(select(Album).where(Album.id == album_id))

    if not db_album:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Rating must be provided.',
        )

    db_album.playing = False
    db_album.rating = rating

    session.add(db_album)
    session.commit()
    session.refresh(db_album)

    db_next = session.scalar(select(Album).where(Album.id == album_id - 1))
    db_next.playing = True

    session.add(db_next)
    session.commit()
    session.refresh(db_next)

    return templates.TemplateResponse(
        'album/playing.html', {'request': request, 'albums': [db_next]}
    )
