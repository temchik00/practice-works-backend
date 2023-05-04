from calendar import timegm
from datetime import datetime
from functools import lru_cache

from redis import Redis

from app.dependencies.settings import get_redis_settings
from app.schemas.auth_schemas import TokenPayload


@lru_cache()
def get_redis_client() -> Redis:
    settings = get_redis_settings()
    return Redis(
        host=settings.host, password=settings.password, decode_responses=True
    )


class RedisTokenStorage:
    client: Redis

    def __init__(self):
        self.client = get_redis_client()

    def add_token(self, token: TokenPayload) -> None:
        time_left = token.exp - timegm(datetime.utcnow().utctimetuple())
        if time_left > 0:
            self.client.set(f"Token {token.jti}", " ", ex=time_left)

    def has_token(self, token: TokenPayload) -> bool:
        if _ := self.client.get(f"Token {token.jti}"):
            return True
        return False


@lru_cache()
def get_token_storage() -> RedisTokenStorage:
    return RedisTokenStorage()
