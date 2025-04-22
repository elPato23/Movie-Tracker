from typing import Literal
from pydantic import field_validator
from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    moviedb_api_key: str
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"
    local_files_dir: str = "files"
    hostname: str = "0.0.0.0"
    port: int = 8000

    @field_validator("log_level", mode="before")
    def validate_log_level(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
