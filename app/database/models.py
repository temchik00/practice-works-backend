from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(63), unique=True, nullable=False)
    passhash = Column(Text, nullable=False)
    first_name = Column(String(40))
    last_name = Column(String(40))
    date_created = Column(DateTime, server_default=func.now(), nullable=False)
    chats = relationship("UserChat", back_populates="user")


class Chat(Base):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True)
    name = Column(String(63), nullable=False)
    messages = relationship("Message")
    users = relationship("UserChat", back_populates="chat")


class UserChat(Base):
    __tablename__ = "user_chat"
    user_id = Column(ForeignKey("user.id"), primary_key=True)
    chat_id = Column(ForeignKey("chat.id"), primary_key=True)
    user = relationship("User", back_populates="chats")
    chat = relationship("Chat", back_populates="users")


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id"), nullable=False)
    chat_id = Column(ForeignKey("chat.id"), nullable=False)
    date_send = Column(DateTime, server_default=func.now(), nullable=False)
    content = Column(Text, nullable=False)
