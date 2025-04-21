from typing import Literal, TypedDict

from tracker.query.base import TVMovieDB, APIPage, TrendingTimeframe
from tracker.query.model import Show, TVShowLength


class TVShowReferenceDict(TypedDict):
    # This is from the TMDB API
    adult: bool
    backdrop_path: str
    genre_ids: list[int]
    id: int
    name: str
    overview: str
    origin_country: list[str]
    original_language: str
    original_name: str
    popularity: float
    poster_path: str
    first_air_date: str
    vote_average: float
    vote_count: int


class TVShowSeriesEpisodeDict(TypedDict):
    id: int
    name: str
    overview: str
    vote_average: float
    vote_count: int
    air_date: str
    episode_number: int
    episode_type: str
    production_code: str
    runtime: int
    season_number: int
    show_id: int
    still_path: str


class TVShowSeriesNetworkDict(TypedDict):
    id: int
    logo_path: str
    name: str
    origin_country: str


class GenreDict(TypedDict):
    id: int
    name: str


class TVShowSeriesDict(TypedDict):
    adult: bool
    backdrop_path: str
    created_by: list[dict]
    episode_run_time: list[int]
    first_air_date: str
    genres: list[GenreDict]
    homepage: str
    id: int
    in_production: bool
    languages: list[str]
    last_air_date: str
    last_episode_to_air: TVShowSeriesEpisodeDict
    name: str
    next_episode_to_air: TVShowSeriesEpisodeDict | None
    networks: list[TVShowSeriesNetworkDict]


class TelevisionDB(TVMovieDB):
    def get_genres(self) -> dict:
        response = self.request("/genre/tv/list", params={"language": "en-US"})
        return response

    def search(
        self, query: str, include_adult: bool = False
    ) -> APIPage[TVShowReferenceDict]:
        response = self.request(
            "/search/tv",
            params={
                "query": query,
                "include_adult": include_adult,
                "language": "en-US",
                "page": "1",
            },
        )
        return response

    def get_trending(
        self, timeframe: TrendingTimeframe
    ) -> APIPage[TVShowReferenceDict]:
        response = self.request(
            f"/trending/tv/{timeframe}",
            params={"language": "en-US"},
        )
        return response

    def get_series(self, series_id: int) -> TVShowSeriesDict:
        response = self.request(f"/tv/{series_id}", params={"language": "en-US"})
        return response


class TVShowAdapter:
    def __init__(self, tv_db: TelevisionDB):
        self.tv_db = tv_db
        self.genres_by_id = {
            genre["id"]: genre["name"] for genre in tv_db.get_genres()["genres"]
        }

    def hydrate_tvshow(self, show_reference: TVShowReferenceDict):
        series = self.tv_db.get_series(show_reference["id"])
        return Show(
            name=show_reference["name"],
            description=show_reference["overview"],
            genres=[self.genres_by_id[genre] for genre in show_reference["genre_ids"]],
            length=TVShowLength(
                seasons=series["number_of_seasons"],
                episodes_per_season={
                    item["season_number"]: item["episode_count"]
                    for item in series["seasons"]
                },
            ),
            networks=[network["name"] for network in series["networks"]],
        )

    def search(self, query: str) -> list[Show]:
        page = self.tv_db.search(query)
        items = page["results"]
        results = []
        for item in items:
            results.append(self.hydrate_tvshow(item))
        return results

    def trending(self, timeframe: TrendingTimeframe) -> list[Show]:
        page = self.tv_db.get_trending(timeframe)
        items = page["results"]
        results = []
        for item in items:
            results.append(self.hydrate_tvshow(item))
        return results
