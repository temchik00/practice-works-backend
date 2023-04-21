from functools import lru_cache
from app.settings import (AuthSettings, DatabaseSettings, FastApiSettings,
                          RedisSettings)


@lru_cache()
def get_database_settings():
    return DatabaseSettings()


@lru_cache()
def get_auth_settings():
    return AuthSettings()


@lru_cache()
def get_fastapi_settings():
    return FastApiSettings()


@lru_cache()
def get_redis_settings():
    return RedisSettings()
