from pydantic import computed_field
from pydantic.dataclasses import dataclass
from datetime import timedelta
from functools import cached_property


@dataclass
class TVShowLength:
    seasons: int
    episodes_per_season: dict[int, int]

    @computed_field
    @cached_property
    def episodes(self) -> int:
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
