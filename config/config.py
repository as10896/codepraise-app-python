import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_URL: str


class Test(Settings):
    environment = "test"

    class Config:
        env_file = "config/env/.env"
        env_file_encoding = "utf-8"


class Development(Settings):
    environment = "development"

    class Config:
        env_file = "config/env/.env.dev"
        env_file_encoding = "utf-8"


class Production(Settings):
    environment = "production"

    class Config:
        env_file = "config/env/.env.prod"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings(mode: str = None, **kwargs) -> Settings:
    env = mode if mode else os.getenv("ENV", "development")
    return {"test": Test, "development": Development, "production": Production,}.get(
        env
    )(**kwargs)
