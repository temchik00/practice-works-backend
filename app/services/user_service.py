from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud.user import get_user_by_id, update_user
from app.database.models import User
from app.dependencies.database import get_db
from app.schemas.user_schemas import UserGetSchema, UserUpdateSchema
from app.services.auth_service import get_current_user
from app.services.exceptions import NotFoundError


def me_service(
    user: User = Depends(get_current_user)
) -> UserGetSchema:
    return UserGetSchema.from_orm(user)


def user_by_id_service(
    user: User | None = Depends(get_user_by_id)
) -> UserGetSchema:
    if user is None:
        raise NotFoundError("Couldn't find user")
    return UserGetSchema.from_orm(user)


def update_user_service(
    user_schema: UserUpdateSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserGetSchema:
    user = update_user(user_schema, user, db)
    return UserGetSchema.from_orm(user)
