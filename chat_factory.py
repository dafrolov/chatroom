from twisted.internet.protocol import Factory
from sqlalchemy.orm import sessionmaker

from chat_protocol import ChatProtocol
from db import engine


class ChatFactory(Factory):

    def __init__(self):
        self.session = sessionmaker(bind=engine)()

        self.chats_by_users = {}
        self.users_by_rooms = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)
