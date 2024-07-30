import factory

from top_albums.models.album import Album


class AlbumFactory(factory.Factory):
    class Meta:
        model = Album

    id = factory.Sequence(lambda n: n + 1)
    name = factory.LazyAttribute(lambda obj: f'album name {obj.id}')
    artist = factory.LazyAttribute(lambda obj: f'artist name {obj.id}')
    label = factory.LazyAttribute(lambda obj: f'label name {obj.id}')
    year = factory.Sequence(lambda n: n + 1999)
    rating = factory.Sequence(lambda n: n)
