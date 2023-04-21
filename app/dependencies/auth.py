from fastapi.security import OAuth2PasswordBearer
from functools import lru_cache

from app.dependencies.settings import get_fastapi_settings


@lru_cache()
def get_oauth_scheme():
    return OAuth2PasswordBearer(
        tokenUrl=f"{get_fastapi_settings().base_path}/auth/signin"
    )
