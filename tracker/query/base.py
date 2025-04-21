import os
import time

import requests

from typing import Generic, TypeVar, TypedDict
from enum import Enum

TResponse = TypeVar("TResponse", bound=dict)


class TrendingTimeframe(str, Enum):
    DAY = "day"
    WEEK = "week"


class APIPage(Generic[TResponse], TypedDict):
    page: int
    results: list[TResponse]
    total_pages: int
    total_results: int


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
