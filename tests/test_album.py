from http import HTTPStatus

from .factories import AlbumFactory


def test_create_album(client):
    response = client.post(
        '/albums/',
        json={
            'id': 1,
            'name': 'test name',
            'artist': 'test artist',
            'label': 'test label',
            'year': 2000,
            'rating': 10,
        },
    )

    assert response.json() == {
        'id': 1,
        'name': 'test name',
        'artist': 'test artist',
        'label': 'test label',
        'year': 2000,
        'rating': 10,
    }


def test_create_existing_album(client, session):
    session.bulk_save_objects(AlbumFactory.create_batch(5))
    session.commit()

    response = client.post(
        '/albums/',
        json={
            'id': 1,
            'name': 'test name',
            'artist': 'test artist',
            'label': 'test label',
            'year': 2000,
            'rating': 10,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Album already exists'}


def test_list_albums_should_return_10_albums(client, session):
    session.bulk_save_objects(AlbumFactory.create_batch(10))
    session.commit()

    response = client.get('/albums/?name=album name')

    assert response.status_code == HTTPStatus.OK
    assert b'<title>List Albums</title>' in response.content


def test_list_albums_no_filter(client):
    response = client.get('/albums/?')

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'At least one filter parameter must be provided.'
    }


def test_get_search_form(client):
    response = client.get('/albums/search')

    assert response.status_code == HTTPStatus.OK
    assert b'<title>Pagina de Busca</title>' in response.content


def test_get_playing_now(client):
    response = client.get('/albums/playing')

    assert response.status_code == HTTPStatus.OK
    assert b'<title>Playing</title>' in response.content


def test_update_rating_album_invalid(client, session):
    session.bulk_save_objects(AlbumFactory.create_batch(5))
    session.commit()

    response = client.post(
        '/albums/100',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Rating must be provided.'}


def test_update_rating_album(client, session):
    session.bulk_save_objects(AlbumFactory.create_batch(5))
    session.commit()

    response = client.post(
        '/albums/25',
        json={
            'rating': 10,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert b'<title>Playing</title>' in response.content
