from typing import Iterable

from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud.message import create_message, get_messages
from app.database.models import Message, User
from app.dependencies.database import get_db
from app.schemas.chat_schemas import ChatGetSchema
from app.schemas.message_schemas import MessageCreateSchema, MessageGetSchema
from app.services.auth_service import get_current_user
from app.services.chat_service import get_chat_by_id_service


def create_message_service(
    schema: MessageCreateSchema,
    user: User = Depends(get_current_user),
    chat: ChatGetSchema = Depends(get_chat_by_id_service),
    db: Session = Depends(get_db),
) -> MessageGetSchema:
    message = create_message(user.id, chat.id, schema, db)
    return MessageGetSchema.from_orm(message)


def get_messages_service(
    user: User = Depends(get_current_user),
    chat: ChatGetSchema = Depends(get_chat_by_id_service),
    messages: Iterable[Message] = Depends(get_messages),
) -> Iterable[MessageGetSchema]:
    return (MessageGetSchema.from_orm(message) for message in messages)
