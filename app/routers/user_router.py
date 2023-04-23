from fastapi import Depends, APIRouter, status

from app.schemas.user_schemas import UserGetSchema
from app.services.user_service import (me_service, user_by_id_service,
                                       update_user_service)


router = APIRouter(prefix="/user", tags=["User"])


@router.get(
    '/me',
    response_model=UserGetSchema,
    summary="Получение информации по текущему пользователю через токен",
    status_code=status.HTTP_200_OK
)
def me(
    user: UserGetSchema = Depends(me_service)
):
    return user


@router.get(
    '/{user_id}',
    response_model=UserGetSchema,
    summary="Получение информации о пользователе по id",
    status_code=status.HTTP_200_OK
)
def user_by_id(
    user: UserGetSchema = Depends(user_by_id_service)
):
    return user


@router.patch(
    '/',
    response_model=UserGetSchema,
    summary="Обновление информации о пользователе",
    status_code=status.HTTP_200_OK
)
def update_user(
    user: UserGetSchema = Depends(update_user_service)
):
    return user