from typing import Iterable

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.crud.exceptions import AlreadyExistsError, CrudError
from app.database.models import User
from app.dependencies.database import get_db
from app.dependencies.settings import get_auth_settings
from app.schemas.user_schemas import UserCreateSchema, UserUpdateSchema


def get_password_hash(password):
    return get_auth_settings().pwd_context.hash(password)


def get_user_by_name(
    username: str, db: Session = Depends(get_db)
) -> User | None:
    if user := db.query(User).filter(User.username == username).first():
        return user
    return None


def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> User | None:
    if user := db.query(User).filter(User.id == user_id).first():
        return user
    return None


def create_user(
    user_schema: UserCreateSchema, db: Session = Depends(get_db)
) -> User:
    try:
        passhash = get_password_hash(user_schema.password)
        user_dict = user_schema.dict(
            exclude_unset=True, exclude_none=True, exclude={"password"}
        )
        user_dict["passhash"] = passhash
        db_user = User(**user_dict)
        db.add(db_user)
        db.commit()
    except IntegrityError as exc:
        raise AlreadyExistsError("Username already taken") from exc
    except SQLAlchemyError as exc:
        raise CrudError("") from exc

    db.refresh(db_user)
    return db_user


def update_user(
    user_schema: UserUpdateSchema,
    db_user: User,
    db: Session = Depends(get_db),
) -> User:
    user_dict = user_schema.dict(
        exclude_unset=True, exclude_none=True, exclude={"password"}
    )
    if user_schema.password:
        user_dict["passhash"] = get_password_hash(user_schema.password)
    for key, value in user_dict.items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)
    try:
        db.add(db_user)
        db.commit()
    except SQLAlchemyError as exc:
        raise CrudError("") from exc
    db.refresh(db_user)
    return db_user


def search_user(
    match: str | None = None,
    limit: int = 5,
    db: Session = Depends(get_db)
) -> Iterable[User]:
    query = db.query(User)
    if match:
        query = query.filter(
            func.lower(User.username).contains(func.lower(match))
        )

    return query.order_by(User.id).limit(limit).all()
