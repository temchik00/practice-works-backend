from typing import Iterable, Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.models import Message
from app.dependencies.database import get_db
from app.schemas.message_schemas import MessageCreateSchema


def create_message(
    user_id: int,
    chat_id: int,
    message_schema: MessageCreateSchema,
    db: Session = Depends(get_db),
) -> Message:
    message_dict = message_schema.dict()
    message_dict["user_id"] = user_id
    message_dict["chat_id"] = chat_id
    db_message = Message(**message_dict)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_messages(
    chat_id: int,
    page_size: int = 100,
    start: Optional[int] = None,
    db: Session = Depends(get_db),
) -> Iterable[Message]:
    query = db.query(Message).filter(Message.chat_id == chat_id)
    if start:
        query = query.order_by(Message.id.asc()).filter(Message.id >= start)
    else:
        query = query.order_by(Message.id.desc())
    query = query.limit(page_size)
    res = query.all()
    return res if start is not None else res[::-1]
