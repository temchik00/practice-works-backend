from passlib.context import CryptContext
from pydantic import BaseSettings, validator


class AuthSettings(BaseSettings):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    private_key: str
    public_key: str
    algorithm = "RS256"
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    class Config:
        env_prefix = "jwt_"
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("private_key")
    @classmethod
    def download_private_key(cls, value):
        with open(value, "r") as file:
            return file.read()

    @validator("public_key")
    @classmethod
    def download_public_key(cls, value):
        with open(value, "r") as file:
            return file.read()


class DatabaseSettings(BaseSettings):
    connection_string: str
    application_name: str

    class Config:
        env_prefix = "db_"
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


class FastApiSettings(BaseSettings):
    base_path: str

    class Config:
        env_prefix = "service_"
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


class RedisSettings(BaseSettings):
    host: str
    password: str

    class Config:
        env_prefix = "redis_"
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
