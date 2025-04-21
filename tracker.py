from typing import Literal
from dataclasses import dataclass
from functools import cached_property
from datetime import timedelta
import time
import os

import requests


class TVMovieDB:
    def __init__(self) -> None:
        self.base_url = "https://api.themoviedb.org/3"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {os.getenv('MOVIEDB_API_KEY')}",
        }
        self.max_requests_per_second = 4
        self.current_request_count = 0

    def request(self, path: str, params: dict):
        # Add something to cache the responses so that we can deal with them later.
        if self.current_request_count >= 4:
            self.current_request_count = 0
            time.sleep(1)
        self.current_request_count += 1
        return requests.get(
            f"{self.base_url}{path}", headers=self.headers, params=params
        ).json()


class MoviesDB(TVMovieDB):
    def get_genres(self) -> dict:
        response = self.request(
            "/genre/movie/list",
            params={"language": "en-US"},
        )
        return response

    def search(self, query: str, include_adult: bool = False) -> dict:
        response = self.request(
            "/search/movie",
            params={
                "query": query,
                "include_adult": include_adult,
                "language": "en-US",
                "page": "1",
            },
        )
        return response

    def get_trending(self, timeframe: Literal["day", "week"]) -> dict:
        response = self.request(
            f"/trending/movie/{timeframe}",
            params={"language": "en-US"},
        )
        return response


class TelevisionDB(TVMovieDB):
    def get_genres(self) -> dict:
        response = self.request("/genre/tv/list", params={"language": "en-US"})
        return response

    def search(self, query: str, include_adult: bool = False) -> dict:
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

    def get_trending(self, timeframe: Literal["day", "week"]) -> dict:
        response = self.request(
            f"/trending/tv/{timeframe}",
            params={"language": "en-US"},
        )
        return response

    def get_series(self, series_id: int):
        response = self.request(f"/tv/{series_id}", params={"language": "en-US"})
        return response


@dataclass
class TVShowLength:
    seasons: int
    episodes_per_season: dict[int, int]

    @cached_property
    def episodes(self):
        return sum(self.episodes_per_season.values())


@dataclass
class MovieLength:
    duration: timedelta


@dataclass
class Show:
    name: str
    description: str
    genres: list[str]
    length: TVShowLength | MovieLength
    networks: list[str]


class TVShowAdapter:
    def __init__(self, tv_db: TelevisionDB):
        self.tv_db = tv_db
        self.genres_by_id = {
            genre["id"]: genre["name"] for genre in tv_db.get_genres()["genres"]
        }

    def hydrate_tvshow(self, show_reference: dict):
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

    def trending(self, timeframe: Literal["day", "week"]) -> list[Show]:
        page = self.tv_db.get_trending(timeframe)
        items = page["results"]
        results = []
        for item in items:
            results.append(self.hydrate_tvshow(item))
        return results


class MovieShowAdapter:
    pass


tv_adapter = TVShowAdapter(TelevisionDB())
trending = tv_adapter.search("How I Met your Mother")
for show in trending:
    print(show.name)
    print(show.description)
    print(
        "Total Seasons:", show.length.seasons, "Total Episodes:", show.length.episodes
    )
    print(show.genres)
    print(show.networks)
    print("--" * 20)
