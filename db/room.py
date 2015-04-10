from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship, backref

from db import Base
from relations import RoomToMessage


class Room(Base):
    __tablename__ = "Room"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    messages = relationship('Message', secondary=RoomToMessage, backref='room')

    def __init__(self, name):
        self.name = name
