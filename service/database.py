import sqlalchemy.orm
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from models import Base

engine = create_engine('sqlite:///video_conference.db')

Base.metadata.create_all(engine)

SessionMaker = sessionmaker(bind=engine, expire_on_commit=False)


def get_session():
    return SessionMaker()
