from functools import lru_cache
from app.settings import DatabaseSettings


@lru_cache()
def get_database_settings():
    return DatabaseSettings()
