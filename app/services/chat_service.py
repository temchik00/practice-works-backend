from typing import Iterable

from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud.chat import (add_user_to_chat, create_chat, get_chat_by_id,
                           user_in_chat)
from app.database.models import Chat, User
from app.dependencies.database import get_db
from app.schemas.chat_schemas import (AddUserSchema, ChatCreateSchema,
                                      ChatGetSchema)
from app.schemas.user_schemas import UserGetSchema
from app.services.auth_service import get_current_user
from app.services.exceptions import NotFoundError


def create_chat_service(
    chat_schema: ChatCreateSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ChatGetSchema:
    chat = create_chat(chat_schema, db)
    add_user_to_chat(chat.id, AddUserSchema(user_id=user.id), db)
    return ChatGetSchema.from_orm(chat)


def add_user_service(
    chat_id: int,
    schema: AddUserSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    if not user_in_chat(user.id, chat_id, db):
        raise NotFoundError("No chat")
    add_user_to_chat(chat_id, schema, db)
    return


def get_chat_by_id_service(
    user: User = Depends(get_current_user),
    chat: Chat = Depends(get_chat_by_id),
    db: Session = Depends(get_db),
) -> ChatGetSchema:
    if chat is None:
        raise NotFoundError("No chat")
    if user_in_chat(user.id, chat.id, db):
        return ChatGetSchema.from_orm(chat)
    raise NotFoundError("No chat")


def get_user_chats_service(
    user: User = Depends(get_current_user),
) -> Iterable[ChatGetSchema]:
    return (ChatGetSchema.from_orm(user_chat.chat) for user_chat in user.chats)


def get_chat_users_service(
    user: User = Depends(get_current_user),
    chat: Chat = Depends(get_chat_by_id),
    db: Session = Depends(get_db),
) -> Iterable[UserGetSchema]:
    if chat is None:
        raise NotFoundError("No chat")
    if user_in_chat(user.id, chat.id, db):
        return (
            UserGetSchema.from_orm(user_chat.user) for user_chat in chat.users
        )
    raise NotFoundError("No chat")


# Чаты пользователя
# Сообщения
