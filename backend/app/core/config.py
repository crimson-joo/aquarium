from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Aquarium"
    data_dir: Path = Field(default=Path("../data"), alias="AQUARIUM_DATA_DIR")
    default_locale: str = Field(default="ko", alias="AQUARIUM_DEFAULT_LOCALE")


@lru_cache
def get_settings() -> Settings:
    return Settings()
