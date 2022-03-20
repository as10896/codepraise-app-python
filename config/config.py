import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_HOST: str
    API_VER: str
    SESSION_SECRET: str


class Test(Settings):
    environment = "test"
    APP_URL: str
    REMOTE_CHROME: str = None

    class Config:
        env_file = "config/env/test.env"
        env_file_encoding = "utf-8"
        secrets_dir = "config/secrets/test"


class Development(Settings):
    environment = "development"

    class Config:
        env_file = "config/env/dev.env"
        env_file_encoding = "utf-8"
        secrets_dir = "config/secrets/dev"


class Production(Settings):
    environment = "production"

    class Config:
        env_file = "config/env/prod.env"
        env_file_encoding = "utf-8"
        secrets_dir = "config/secrets/prod"


@lru_cache()
def get_settings(mode: str = None, **kwargs) -> Settings:
    env = mode if mode else os.getenv("ENV", "development")
    return {"test": Test, "development": Development, "production": Production,}.get(
        env
    )(**kwargs)
