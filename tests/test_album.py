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
    expected_albums = 10
    session.bulk_save_objects(AlbumFactory.create_batch(10))
    session.commit()

    response = client.get('/albums/?name=album name')

    assert len(response.json()['Albums']) == expected_albums


def test_list_albums_should_return_1_albums(client, session):
    expected_albums = 1
    session.bulk_save_objects(AlbumFactory.create_batch(10))
    session.commit()

    response = client.get('/albums/?year=2015')

    assert len(response.json()['Albums']) == expected_albums


def test_list_albums_no_filter(client):
    response = client.get('/albums/?')

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'At least one filter parameter must be provided.'
    }
