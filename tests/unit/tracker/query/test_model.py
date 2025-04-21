from tracker.query.model import TVShowLength


def test_tvshow_length__when_given_a_set_of_seasons__computes_episodes_as_expected():
    season_breakdown = {
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 6,
        7: 7,
    }

    tvshow_length = TVShowLength(seasons=7, episodes_per_season=season_breakdown)

    assert tvshow_length.episodes == 28
