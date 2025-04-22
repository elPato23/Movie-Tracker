from enum import Enum
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


class ImageType(str, Enum):
    backdrop: str = "backdrop"
    poster: str = "poster"


@dataclass
class Image:
    show_id: int
    image_type: ImageType

    @computed_field
    @cached_property
    def small(self) -> str:
        return f"/images/small/{self.show_id}_{self.image_type}.png"

    @computed_field
    @cached_property
    def medium(self) -> str:
        return f"/images/medium/{self.show_id}_{self.image_type}.png"

    @computed_field
    @cached_property
    def large(self) -> str:
        return f"/images/large/{self.show_id}_{self.image_type}.png"


@dataclass
class Show:
    name: str
    description: str
    genres: list[str]
    length: TVShowLength | MovieLength
    networks: list[str]
    banner: Image | None = None
    poster: Image | None = None
