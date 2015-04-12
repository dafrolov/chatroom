import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

import config


if not config.testing:
    db = 'sqlite:///chatroom.db'
else:
    db = 'sqlite:///chatroom_testing.db'
    if os.path.exists(db):
        os.remove(db)


engine = create_engine(db, echo=True)
Base = declarative_base()


import relations
import user
import room
import message

Base.metadata.create_all(engine)
