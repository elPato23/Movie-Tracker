from typing import TypedDict

from tracker.query.base import TVMovieDB, TrendingTimeframe
from tracker.query.images import ImageDownloader
from tracker.query.model import Image, ImageType, Show, TVShowLength


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


class APIPage(TypedDict):
    page: int
    results: list[TVShowReferenceDict]
    total_pages: int
    total_results: int


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
        self,
        query: str,
        include_adult: bool = False,
    ) -> APIPage:
        """Searches for TV Shows with the given name in the query

        Args:
            query (str): Search Terms to try and find shows
            include_adult (bool, optional): Whether to include adult content. Defaults to False.

        Returns:
            APIPage[TVShowReferenceDict]: API Page object of with results of type TVShowReferenceDict
        """
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
    def __init__(self, tv_db: TelevisionDB, image_downloader: ImageDownloader = None):
        self.image_downloader = image_downloader
        self.tv_db = tv_db
        self.genres_by_id = {
            genre["id"]: genre["name"] for genre in tv_db.get_genres()["genres"]
        }

    def hydrate_tvshow(
        self,
        show_reference: TVShowReferenceDict,
        with_images: bool = False,
    ) -> Show:
        series = self.tv_db.get_series(show_reference["id"])
        banner = None
        poster = None
        if with_images:
            if self.image_downloader is None:
                raise ValueError("Image Downloader must be set if with_images is True")

            if show_reference["backdrop_path"] is not None:
                banner = Image(
                    image_type=ImageType.backdrop, show_id=show_reference["id"]
                )
                self.image_downloader.download(banner, show_reference["backdrop_path"])

            if show_reference["poster_path"] is not None:
                poster = Image(
                    image_type=ImageType.poster, show_id=show_reference["id"]
                )
                self.image_downloader.download(poster, show_reference["poster_path"])

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
            banner=banner,
            poster=poster,
        )

    def search(
        self,
        query: str,
        with_images: bool = False,
    ) -> list[Show]:
        page = self.tv_db.search(query)
        items = page["results"]
        results = []
        for item in items:
            results.append(self.hydrate_tvshow(item, with_images=with_images))
        return results

    def trending(
        self,
        timeframe: TrendingTimeframe,
        with_images: bool = False,
    ) -> list[Show]:
        page = self.tv_db.get_trending(timeframe)
        items = page["results"]
        results = []
        for item in items:
            results.append(self.hydrate_tvshow(item, with_images=with_images))
        return results
