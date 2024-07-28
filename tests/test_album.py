from http import HTTPStatus

from .factories import AlbumFactory


def test_create_album(client):
    response = client.post(
        '/album/',
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
        '/album/',
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
