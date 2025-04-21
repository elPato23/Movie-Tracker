from dataclasses import asdict
from functools import cache
import logging
from logging.config import dictConfig
import sys

from typing import Generic, TypeVar
from pydantic import BaseModel
from typing_extensions import Literal, TypedDict
from fastapi import APIRouter, Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from tracker import __version__
from .query.base import TrendingTimeframe
from .query.model import Show
from .config import APISettings
from .query.tvshows import TVShowAdapter, TelevisionDB


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
    return TVShowAdapter(TelevisionDB())


TVar = TypeVar("TVar", bound=BaseModel)


class Page(
    BaseModel,
    Generic[TVar],
):
    results: list[TVar]


@api_router.get("/tv/trending/{timeframe}", response_model=Page[Show])
def get_trending_tv_shows(
    timeframe: TrendingTimeframe,
    adapter: TVShowAdapter = Depends(tv_adapter),
):
    trending_shows = adapter.trending(timeframe)
    return {"results": [asdict(show) for show in trending_shows]}


@api_router.get("/tv/search/", response_model=Page[Show])
def get_trending_tv_shows(
    query: str = Query(),
    adapter: TVShowAdapter = Depends(tv_adapter),
):
    # TODO: Add pagination to the API so we can keep going with each page.
    trending_shows = adapter.search(query)
    return {"results": [asdict(show) for show in trending_shows]}


app.include_router(api_router)


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
