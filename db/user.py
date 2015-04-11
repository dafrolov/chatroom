from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship, backref

from db import Base


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    salt = Column(String)
    hash = Column(String)

    messages = relationship('Message', backref='user', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def set_salt(self, salt):
        self.salt = salt

    def set_hash(self, hash):
        self.hash = hash
