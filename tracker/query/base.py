import os
import time

import requests

from enum import Enum


class TrendingTimeframe(str, Enum):
    DAY = "day"
    WEEK = "week"


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

    def request_stream(self, path: str, params: dict):
        if self.current_request_count >= 4:
            self.current_request_count = 0
            time.sleep(1)
        self.current_request_count += 1
        return requests.get(
            f"{self.base_url}{path}",
            headers=self.headers,
            params=params,
            stream=True,
        )
