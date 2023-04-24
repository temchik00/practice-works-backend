from datetime import datetime, timedelta
from fastapi import Depends, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from jose import ExpiredSignatureError, JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from uuid import uuid4

from app.crud.user import get_user_by_name, get_user_by_id, create_user
from app.database.models import User
from app.dependencies.auth import get_oauth_scheme
from app.dependencies.clients import RedisTokenStorage, get_token_storage
from app.dependencies.database import get_db
from app.dependencies.settings import get_auth_settings
from app.schemas.auth_schemas import Token, TokenPayload
from app.services.exceptions import (WrongCredentialsError, UnauthorizedError,
                                     ServiceError)


def verify_password(plain_password, hashed_password):
    return get_auth_settings().pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_token(token_data: TokenPayload) -> str:
    settings = get_auth_settings()
    token = jwt.encode(
        token_data,
        settings.private_key.encode('ascii'),
        algorithm=settings.algorithm
    )
    return token


def authenticate_user(
    user_schema: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> User | None:
    if not (user := get_user_by_name(user_schema.username, db)):
        return None

    if not verify_password(user_schema.password, user.passhash):
        return None

    return user


def create_token_pair(
    user: User | None = Depends(authenticate_user)
) -> tuple[str, str]:
    if user is None:
        raise UnauthorizedError("Wrong username or password")
    settings = get_auth_settings()
    access_data = {
        "sub": str(user.id),
        "name": user.username,
        "iat": datetime.utcnow(),
        "jti": str(uuid4()),
        "exp": (
            datetime.utcnow() +
            timedelta(minutes=settings.access_token_expire_minutes)
        )
    }
    refresh_data = {
        "sub": str(user.id),
        "name": user.username,
        "iat": datetime.utcnow(),
        "jti": str(uuid4()),
        "exp": (
            datetime.utcnow() +
            timedelta(days=settings.refresh_token_expire_days)
        )
    }
    access_token = create_token(access_data)
    refresh_token = create_token(refresh_data)
    return access_token, refresh_token


def signin_service(
    response: Response,
    tokens: tuple[str, str] = Depends(create_token_pair)
) -> Token:
    access_token, refresh_token = tokens
    response.set_cookie(key="Authorization", value=refresh_token)
    return Token(access_token=access_token)


def decode_token_payload(
    token: str = Depends(get_oauth_scheme())
) -> dict[str, any]:
    settings = get_auth_settings()
    try:
        return jwt.decode(
            token,
            settings.public_key,
            algorithms=[settings.algorithm]
        )
    except ExpiredSignatureError as exc:
        raise UnauthorizedError("Token expired") from exc
    except (JWTError, ValidationError) as exc:
        raise ServiceError("Wrong token") from exc


def decode_token(
    token_payload: dict[str, any] = Depends(decode_token_payload)
) -> TokenPayload:
    return TokenPayload(**token_payload)


def is_token_not_invalidated(
    token_payload: TokenPayload = Depends(decode_token),
    token_storage: RedisTokenStorage = Depends(get_token_storage)
) -> bool:
    if token_storage.has_token(token_payload):
        raise UnauthorizedError("Token invalidated")
    return True


def get_current_user(
    _: bool = Depends(is_token_not_invalidated),
    token_payload: TokenPayload = Depends(decode_token),
    db: Session = Depends(get_db)
) -> User:
    user_id = token_payload.sub
    username = token_payload.name
    if user_id is None or username is None:
        raise WrongCredentialsError("Wrong token")

    user = get_user_by_id(user_id, db)
    if user is None or user.username != username:
        raise WrongCredentialsError("No such user")
    return user


def create_tokens_from_refresh(
    Authorization: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if not Authorization:
        raise UnauthorizedError("No refresh token")

    token_data = decode_token_payload(Authorization)
    user = get_current_user(True, TokenPayload(**token_data), db)
    return create_token_pair(user)


def refresh_service(
    response: Response,
    tokens: tuple[str, str] = Depends(create_tokens_from_refresh)
) -> Token:
    access_token, refresh_token = tokens
    response.set_cookie(key="Authorization", value=refresh_token)
    return Token(access_token=access_token)


def signup_service(
    response: Response,
    user: User = Depends(create_user)
) -> Token:
    access_token, refresh_token = create_token_pair(user)
    response.set_cookie(key="Authorization", value=refresh_token)
    return Token(access_token=access_token)


def invalidate_access_token(
    token_payload: TokenPayload = Depends(decode_token),
    token_storage: RedisTokenStorage = Depends(get_token_storage)
) -> None:
    token_storage.add_token(token_payload)


def logout_service(
    _: None = Depends(invalidate_access_token)
) -> None:
    return
