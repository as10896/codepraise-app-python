import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_URL: str
    SESSION_SECRET: str


class Test(Settings):
    environment = "test"
    APP_URL: str

    class Config:
        env_file = "config/env/.env"
        env_file_encoding = "utf-8"
        secrets_dir = "config/secrets/test"


class Development(Settings):
    environment = "development"

    class Config:
        env_file = "config/env/.env.dev"
        env_file_encoding = "utf-8"
        secrets_dir = "config/secrets/dev"


class Production(Settings):
    environment = "production"

    class Config:
        env_file = "config/env/.env.prod"
        env_file_encoding = "utf-8"
        secrets_dir = "config/secrets/prod"


@lru_cache()
def get_settings(mode: str = None, **kwargs) -> Settings:
    env = mode if mode else os.getenv("ENV", "development")
    return {"test": Test, "development": Development, "production": Production,}.get(
        env
    )(**kwargs)
