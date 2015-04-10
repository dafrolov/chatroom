from sqlalchemy import Column, Date, Integer, String

from db import Base


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    password = Column(String)

    def __init__(self, name):
        self.name = name

    def set_password(self, password):
        self.password = password
