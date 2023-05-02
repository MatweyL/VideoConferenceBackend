import datetime

from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True
    created = Column(TIMESTAMP, default=datetime.datetime.now())


class User(BaseEntity):
    __tablename__ = 'user'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(64), nullable=False, unique=True)
    password_hashed = Column(VARCHAR(128), nullable=False)


class UserInfo(BaseEntity):
    __tablename__ = 'user_info'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    first_name = Column(VARCHAR(64), nullable=True)
    last_name = Column(VARCHAR(64), nullable=True)
