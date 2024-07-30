from top_albums.services.filter_service import build_filter


def test_filter_name():
    filter_list = build_filter('name')

    assert filter_list != []


def test_filter_rating():
    filter_list = build_filter(rating=9.5)

    assert filter_list != []


def test_filter_all_parameters():
    filter_list = build_filter('name', 'artist', 'label', 'year', 'rating')

    assert filter_list != []


def test_filter_no_parameters():
    filter_list = build_filter()

    assert filter_list == []
