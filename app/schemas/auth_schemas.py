from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    type: str = "Bearer"


class TokenPayload(BaseModel):
    jti: str
    sub: str
    name: str
    iat: int
    exp: int
