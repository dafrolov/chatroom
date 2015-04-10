from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///chatroom.db', echo=True)
Base = declarative_base()


import relations
import user
import room
import message

Base.metadata.create_all(engine)
