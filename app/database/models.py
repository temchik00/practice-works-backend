from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(63), unique=True, nullable=False)
    passhash = Column(Text, nullable=False)
    first_name = Column(String(40))
    last_name = Column(String(40))
    date_created = Column(DateTime, server_default=func.now(), nullable=False)
