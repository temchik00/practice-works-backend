from datetime import datetime

import pytz
from pydantic import BaseModel, validator


class MessageBaseSchema(BaseModel):
    content: str

    class Config:
        orm_mode = True


class MessageCreateSchema(MessageBaseSchema):
    pass


class MessageGetSchema(MessageBaseSchema):
    id: int
    chat_id: int
    user_id: int
    date_send: datetime

    @validator("date_send")
    def validate_date_send(cls, value):
        if not isinstance(value, datetime):
            raise ValueError("'date_send' must be datetime")

        if value.tzname() is None:
            return value.astimezone(pytz.UTC)
        return value
