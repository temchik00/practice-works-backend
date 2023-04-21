from fastapi import Depends
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.crud.exceptions import CrudError, AlreadyExistsError
from app.database.models import User
from app.dependencies.database import get_db
from app.dependencies.settings import get_auth_settings
from app.schemas.user_schemas import UserCreateSchema


def get_password_hash(password):
    return get_auth_settings().pwd_context.hash(password)


def get_user_by_name(
    username: str,
    db: Session = Depends(get_db)
) -> User | None:
    if user := db.query(User).filter(User.username == username).first():
        return user
    return None


def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
) -> User | None:
    if user := db.query(User).filter(User.id == user_id).first():
        return user
    return None


def create_user(
    user_schema: UserCreateSchema,
    db: Session = Depends(get_db)
) -> User:
    try:
        passhash = get_password_hash(user_schema.password)
        db_user = User(username=user_schema.username, passhash=passhash)
        db.add(db_user)
        db.commit()
    except IntegrityError as exc:
        raise AlreadyExistsError("Username already taken") from exc
    except SQLAlchemyError as exc:
        raise CrudError("") from exc
    db.refresh(db_user)
    return db_user
