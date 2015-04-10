from twisted.internet.protocol import Factory
from twisted.internet import task
from sqlalchemy.orm import sessionmaker

from chat_protocol import ChatProtocol
from db import engine


class ChatFactory(Factory):
    commit_period = 10

    def __init__(self):
        self.session = sessionmaker(bind=engine)()

        self.chats_by_users = {}
        self.users_by_rooms = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)

    def startCommitLoop(self):  # TODO: split ChatFactory and ChatServer classes
        task.LoopingCall(self.session.commit).start(self.commit_period)