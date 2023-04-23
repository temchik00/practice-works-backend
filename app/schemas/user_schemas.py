import pytz
from datetime import datetime
from pydantic import BaseModel, validator


class UserBaseSchema(BaseModel):
    first_name: str | None
    last_name: str | None

    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
    username: str
    password: str


class UserGetSchema(UserBaseSchema):
    id: int
    username: str
    date_created: datetime

    @validator("date_created")
    def validate_date_created(cls, value):
        if not isinstance(value, datetime):
            raise ValueError("'date_created' must be datetime")

        if value.tzname() is None:
            return value.astimezone(pytz.UTC)
        return value


class UserUpdateSchema(UserBaseSchema):
    password: str | None
