from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from db import Base
from relations import RoomToMessage


class Message(Base):
    __tablename__ = "Message"

    id = Column(Integer, primary_key=True)
    content = Column(String)

    user_id = Column(Integer, ForeignKey('User.id'))
    rooms = relationship('Room', secondary=RoomToMessage, backref='message')

    def __init__(self, user_id, content):
        self.user_id = user_id
        self.content = content
