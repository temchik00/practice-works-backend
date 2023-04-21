from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
    password: str


class UserGetSchema(UserBaseSchema):
    id: int
