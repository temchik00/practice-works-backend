from typing import Iterable

from fastapi import Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.crud.chat import get_chat_by_id
from app.crud.message import create_message, get_messages
from app.database.models import Message, User
from app.dependencies.clients import (ChatSocketsManager, RedisTokenStorage,
                                      get_token_storage)
from app.dependencies.database import get_db
from app.schemas.chat_schemas import ChatGetSchema
from app.schemas.message_schemas import MessageCreateSchema, MessageGetSchema
from app.services.auth_service import (decode_token, decode_token_payload,
                                       get_current_user,
                                       is_token_not_invalidated)
from app.services.chat_service import get_chat_by_id_service

CHATS_MANAGER = ChatSocketsManager()


async def create_message_service(
    schema: MessageCreateSchema,
    user: User = Depends(get_current_user),
    chat: ChatGetSchema = Depends(get_chat_by_id_service),
    db: Session = Depends(get_db),
) -> MessageGetSchema:
    message = create_message(user.id, chat.id, schema, db)
    schema = MessageGetSchema.from_orm(message)
    await CHATS_MANAGER.send_message(chat.id, schema)
    return schema


def get_messages_service(
    user: User = Depends(get_current_user),
    chat: ChatGetSchema = Depends(get_chat_by_id_service),
    messages: Iterable[Message] = Depends(get_messages),
) -> Iterable[MessageGetSchema]:
    return (MessageGetSchema.from_orm(message) for message in messages)


async def connect_message_websocket_service(
    token: str,
    chat_id: int,
    websocket: WebSocket,
    db: Session = Depends(get_db),
    token_storage: RedisTokenStorage = Depends(get_token_storage),
):
    try:
        payload = decode_token_payload(token)
        payload = decode_token(payload)
        is_token_not_invalidated(payload, token_storage)
        user = get_current_user(True, payload, db)
        chat = get_chat_by_id(chat_id, db)
        get_chat_by_id_service(user, chat, db)
    except Exception:
        await websocket.accept()
        await websocket.close(4004, "Chat not found")
        return
    await CHATS_MANAGER.add_user(websocket, chat_id)
    try:
        while True:
            msg = await websocket.receive()
            if msg.get("type") == "websocket.disconnect":
                raise WebSocketDisconnect
    except WebSocketDisconnect:
        CHATS_MANAGER.remove_user(websocket, chat_id)
