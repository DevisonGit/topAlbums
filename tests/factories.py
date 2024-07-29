import factory

from top_albums.models.album import Album


class AlbumFactory(factory.Factory):
    class Meta:
        model = Album

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda obj: f'album name {obj.id}')
    artist = factory.LazyAttribute(lambda obj: f'artist name {obj.id}')
    label = factory.LazyAttribute(lambda obj: f'label name {obj.id}')
    year = 2000
    rating = 10
