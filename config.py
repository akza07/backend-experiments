from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


# Config for appwide condigurations
class AppConfigs(BaseSettings):
    app_name: str = "My Escrow API"
    database_name: str

    stripe_publishable_key: str
    stripe_secret_key: str

    jwt_secret_key: str
    jwt_algorithm: str

    model_config = SettingsConfigDict(env_file=".env")


# reuses the same instance from cache
@lru_cache
def _get_config():
    return AppConfigs()

ENV = _get_config()
