from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# Config for appwide condigurations
class AppConfigs(BaseSettings):
    app_name: str = "My Escrow API"
    database_name: str

    model_config = SettingsConfigDict(env_file=".env")


# reuses the same instance from cache
@lru_cache
def get_config():
    return AppConfigs()

