from typing import Iterable

from fastapi import APIRouter, Depends, Response, status

from app.schemas.chat_schemas import ChatGetSchema
from app.schemas.message_schemas import MessageGetSchema
from app.schemas.user_schemas import UserGetSchema
from app.services.chat_service import (add_user_service, create_chat_service,
                                       get_chat_by_id_service,
                                       get_chat_users_service,
                                       get_user_chats_service)
from app.services.message_service import (create_message_service,
                                          get_messages_service)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post(
    "/{chat_id}/user",
    summary="Добавление пользователя в чат",
    status_code=status.HTTP_204_NO_CONTENT,
)
def add_user_to_chat(_: None = Depends(add_user_service)):
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{chat_id}/users",
    response_model=list[UserGetSchema],
    summary="Получение пользователей чата",
    status_code=status.HTTP_200_OK,
)
def get_chat_users(
    users: Iterable[UserGetSchema] = Depends(get_chat_users_service),
):
    return users


@router.post(
    "/{chat_id}/message",
    response_model=MessageGetSchema,
    summary="Отправка сообщения в чат",
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    message: MessageGetSchema = Depends(create_message_service),
):
    return message


@router.get(
    "/{chat_id}/messages",
    response_model=list[MessageGetSchema],
    summary="Получение сообщений из чата",
    status_code=status.HTTP_200_OK,
)
def get_messages(
    message: Iterable[MessageGetSchema] = Depends(get_messages_service),
):
    return message


@router.get(
    "/my_chats",
    response_model=list[ChatGetSchema],
    summary="Получение чатов пользователя",
    status_code=status.HTTP_200_OK,
)
def get_user_chats(
    chats: Iterable[ChatGetSchema] = Depends(get_user_chats_service),
):
    return chats


@router.get(
    "/{chat_id}",
    response_model=ChatGetSchema,
    summary="Получение чата по id",
    status_code=status.HTTP_200_OK,
)
def get_chat(chat: ChatGetSchema = Depends(get_chat_by_id_service)):
    return chat


@router.post(
    "/",
    response_model=ChatGetSchema,
    summary="Создание нового чата",
    status_code=status.HTTP_201_CREATED,
)
def create_chat(chat: ChatGetSchema = Depends(create_chat_service)):
    return chat
