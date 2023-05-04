from fastapi import Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.database.models import Chat, UserChat
from app.dependencies.database import get_db
from app.schemas.chat_schemas import AddUserSchema, ChatCreateSchema


def create_chat(
    chat_schema: ChatCreateSchema, db: Session = Depends(get_db)
) -> Chat:
    db_chat = Chat(**chat_schema.dict())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def add_user_to_chat(
    chat_id: int, add_user_schema: AddUserSchema, db: Session = Depends(get_db)
) -> None:
    user_chat_dict = add_user_schema.dict()
    user_chat_dict["chat_id"] = chat_id
    user_chat = UserChat(**user_chat_dict)
    db.add(user_chat)
    db.commit()
    return None


def get_chat_by_id(chat_id: int, db: Session = Depends(get_db)) -> Chat | None:
    return db.query(Chat).filter(Chat.id == chat_id).first()


def user_in_chat(
    user_id: int, chat_id: int, db: Session = Depends(get_db)
) -> bool:
    user_chat = (
        db.query(UserChat)
        .filter(and_(UserChat.user_id == user_id, UserChat.chat_id == chat_id))
        .first()
    )
    return user_chat is not None
