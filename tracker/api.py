from dataclasses import asdict
from functools import cache
import logging
from logging.config import dictConfig
import sys

from typing import Generic, TypeVar
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing_extensions import Literal, TypedDict
from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from tracker import __version__
from tracker.query.images import ImageDownloader
from .query.base import TrendingTimeframe
from .query.model import Show
from .config import APISettings
from .query.tvshows import TVShowAdapter, TelevisionDB

logger = logging.getLogger(__name__)
config = APISettings()
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")


class HealthResponse(TypedDict):
    o: Literal["k"]


@api_router.get("/healthz", response_model=HealthResponse)
def healthz() -> dict:
    return {"o": "k"}


class VersionResponse(TypedDict):
    version: str


@api_router.get("/version", response_model=VersionResponse)
def version() -> dict:
    return {"version": __version__}


@cache
def tv_adapter():
    db = TelevisionDB()
    return TVShowAdapter(db, ImageDownloader(db, config.local_files_dir))


TVar = TypeVar("TVar", bound=BaseModel)


class Page(
    BaseModel,
    Generic[TVar],
):
    results: list[TVar]


def download_images(shows: list[Show], image_downloader: ImageDownloader):
    for show in shows:
        if show.banner:
            try:
                image_downloader.download_from_image(show.banner)
            except Exception as e:
                logger.exception(e)
                logger.warning(f"Failed to store banner images: {show}")
        if show.poster:
            try:
                image_downloader.download_from_image(show.poster)
            except Exception as e:
                logger.exception(e)
                logger.warning(f"Failed to store poster images: {show}")


@api_router.get("/tv/trending/{timeframe}", response_model=Page[Show])
def get_trending_tv_shows(
    timeframe: TrendingTimeframe,
    background_tasks: BackgroundTasks,
    adapter: TVShowAdapter = Depends(tv_adapter),
):
    trending_shows = adapter.trending(timeframe)
    background_tasks.add_task(download_images, trending_shows, adapter.image_downloader)
    return {"results": [asdict(show) for show in trending_shows]}


@api_router.get("/tv/search", response_model=Page[Show])
def get_trending_tv_shows(
    background_tasks: BackgroundTasks,
    query: str = Query(),
    adapter: TVShowAdapter = Depends(tv_adapter),
):
    # TODO: Add pagination to the API so we can keep going with each page.
    found_shows = adapter.search(query)
    background_tasks.add_task(download_images, found_shows, adapter.image_downloader)
    return {"results": [asdict(show) for show in found_shows]}


app.include_router(api_router)
app.mount(
    "/",
    StaticFiles(
        directory=config.local_files_dir,
    ),
    name="static",
)


# not covering due to it locking the thread.
def main():  # pragma: no cover
    import uvicorn

    logging_config = {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "default",
            },
            "stderr": {
                "class": "logging.StreamHandler",
                "stream": sys.stderr,
                "formatter": "default",
            },
        },
        "root": {"level": config.log_level, "handlers": ["stdout"]},
        "loggers": {
            "tracker": {
                "level": config.log_level,
                "handlers": ["stdout"],
                "propagate": False,
            },
            "uvicorn": {
                "level": config.log_level,
                "handlers": ["stdout"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": config.log_level,
                "handlers": ["stdout"],
                "propagate": False,
            },
            "uvicorn.error": {
                "level": config.log_level,
                "handlers": ["stderr"],
                "propagate": False,
            },
        },
    }
    dictConfig(logging_config)
    logger = logging.getLogger("uvicorn")
    logger.info(f"Starting server: http://localhost:{config.port}")
    uvicorn.run(
        app,
        host=config.hostname,
        port=config.port,
        log_config=logging_config,
    )


if __name__ == "__main__":
    main()
