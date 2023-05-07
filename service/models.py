import datetime

from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, TIMESTAMP, Text, Boolean
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


class Conference(BaseEntity):
    __tablename__ = "conference"
    id = Column(Text, nullable=False,  primary_key=True, unique=True)
    creator_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    is_finished = Column(Boolean, default=False, nullable=False)
    is_joining_allowed = Column(Boolean, default=True, nullable=False)
    finished = Column(TIMESTAMP)


class ConferenceParticipant(BaseEntity):
    __tablename__ = "conference_participant"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    conference_id = Column(Text, ForeignKey('conference.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    is_banned = Column(Boolean, default=False)
    role = Column(Text, nullable=False, default="user")
