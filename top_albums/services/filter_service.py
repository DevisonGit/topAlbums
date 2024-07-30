from top_albums.models.album import Album


def build_filter(name=None, artist=None, label=None, year=None, rating=None):
    filters = []

    if name:
        filters.append(Album.name.ilike(f'%{name}%'))
    if artist:
        filters.append(Album.name.ilike(f'%{artist}%'))
    if label:
        filters.append(Album.name.ilike(f'%{label}%'))
    if year is not None:
        filters.append(Album.year == year)
    if rating is not None:
        filters.append(Album.rating == rating)

    return filters
