from pydantic import BaseModel


class ChatBaseSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ChatCreateSchema(ChatBaseSchema):
    pass


class ChatGetSchema(ChatBaseSchema):
    id: int


class AddUserSchema(BaseModel):
    user_id: int
