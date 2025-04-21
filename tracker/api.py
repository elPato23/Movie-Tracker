from dataclasses import asdict
from functools import cache
import sys
from fastapi import APIRouter, Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from tracker.query.base import TrendingTimeframe
from .config import APISettings
from logging.config import dictConfig

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


@cache
def tv_adapter():
    return TVShowAdapter(TelevisionDB())


@api_router.get("/tv/trending/{timeframe}")
def get_trending_tv_shows(
    timeframe: TrendingTimeframe,
    adapter: TVShowAdapter = Depends(tv_adapter),
):
    trending_shows = adapter.trending(timeframe)
    return {"results": [asdict(show) for show in trending_shows]}


@api_router.get("/tv/search/")
def get_trending_tv_shows(
    query: str = Query(),
    adapter: TVShowAdapter = Depends(tv_adapter),
):
    # TODO: Add pagination to the API so we can keep going with each page.
    trending_shows = adapter.search(query)
    return {"results": [asdict(show) for show in trending_shows]}


app.include_router(api_router)

if __name__ == "__main__":
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

    uvicorn.run(
        app,
        host=config.hostname,
        port=config.port,
        log_config=logging_config,
    )
