import json
from calendar import timegm
from datetime import datetime
from functools import lru_cache

from fastapi import WebSocket
from redis import Redis

from app.dependencies.settings import get_redis_settings
from app.schemas.auth_schemas import TokenPayload
from app.schemas.message_schemas import MessageGetSchema


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


class BaseWebsocketManager:
    connections: list[WebSocket]

    def __init__(self):
        self.connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)

    def remove(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)


class ChatSocketsManager:
    managers: dict[int, BaseWebsocketManager]

    def __init__(self):
        self.managers = {}

    async def add_user(self, websocket: WebSocket, chat_id: int):
        if chat_id not in self.managers:
            self.managers[chat_id] = BaseWebsocketManager()
        await self.managers[chat_id].connect(websocket)

    def remove_user(self, websocket: WebSocket, chat_id: int):
        if chat_id not in self.managers:
            return
        self.managers[chat_id].remove(websocket)
        if len(self.managers[chat_id].connections) == 0:
            del self.managers[chat_id]

    async def send_message(self, chat_id: int, message: MessageGetSchema):
        if chat_id not in self.managers:
            return
        msg_dict = message.dict()
        msg_dict["date_send"] = str(msg_dict["date_send"])
        msg_str = json.dumps(msg_dict)
        await self.managers[chat_id].broadcast(msg_str)
