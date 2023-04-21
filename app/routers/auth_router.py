from fastapi import APIRouter, status, Depends, Response

from app.schemas.auth_schemas import Token
from app.services.auth_service import (signin_service, refresh_service,
                                       signup_service, logout_service)


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    '/signin',
    response_model=Token,
    summary="Получение токена по логину и паролю",
    status_code=status.HTTP_200_OK
)
def sign_in(
    access_token: Token = Depends(signin_service)
):
    return access_token


@router.post(
    '/signup',
    response_model=Token,
    summary="Регистрация и получение токена по логину и паролю",
    status_code=status.HTTP_201_CREATED
)
def sign_up(
    access_token: Token = Depends(signup_service)
):
    return access_token


@router.post(
    '/refresh',
    response_model=Token,
    summary="Обновление токенов через refresh",
    status_code=status.HTTP_200_OK
)
def refresh(
    access_token: Token = Depends(refresh_service)
):
    return access_token


@router.post(
    '/logout',
    summary="Выход из системы и инвалидация токена",
    status_code=status.HTTP_204_NO_CONTENT
)
def logout(
    response: Response,
    _: None = Depends(logout_service)
):
    response.delete_cookie(key="Authorization")
    response.status_code = status.HTTP_204_NO_CONTENT
    return response
