from functools import lru_cache

from fastapi import Depends
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.dependencies.settings import get_database_settings


@lru_cache()
def get_sql_alchemy_engine() -> Engine:
    settings = get_database_settings()
    return create_engine(
        settings.connection_string,
        pool_pre_ping=True,
        connect_args={"application_name": settings.application_name},
    )


def get_session_local(engine: Engine = Depends(get_sql_alchemy_engine)):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db(session_maker=Depends(get_session_local)) -> Session:
    db: Session = session_maker()
    try:
        yield db
    finally:
        db.close()
