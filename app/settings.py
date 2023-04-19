from passlib.context import CryptContext
from pydantic import BaseSettings


class AuthSettings(BaseSettings):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    private_key: str
    public_key: str
    algorithm = "RS256"
    token_expire_minutes: int
    long_token_expire_days: int

    class Config:
        env_prefix = "jwt_"
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


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
