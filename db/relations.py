from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy.schema import Table

from db import Base


RoomToMessage = Table('RoomToMessage', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('roomId', Integer, ForeignKey('Room.id')),
    Column('messageId', Integer, ForeignKey('Message.id')),
)