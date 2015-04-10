from twisted.internet.protocol import Factory

from chat_protocol import ChatProtocol


class ChatFactory(Factory):

    def __init__(self):
        self.chats_by_users = {}
        self.users_by_rooms = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)
