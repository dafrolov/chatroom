from twisted.protocols.basic import LineReceiver

from command_handler import CommandHandler
from state_handler import StateHandler


class ChatProtocol(LineReceiver, StateHandler, CommandHandler):

    def __init__(self, master):
        self.chats_by_users = master.chats_by_users
        self.users_by_rooms = master.users_by_rooms

        self.name = None
        self.state = 'get_name'

    def connectionMade(self):
        self.sendLine("What's your name?")

    def connectionLost(self, reason):
        if self.name in self.chats_by_users:
            del self.chats_by_users[self.name]

    def lineReceived(self, line):
        if line.startswith('\\'):
            line = line.lstrip('\\')
            self.handle_command(line)
        else:
            self.handle_state(line)

    def distribute_message(self, message, room=None):
        for name, protocol in self.chats_by_users.iteritems():
            if protocol != self and (not room or protocol.name in self.users_by_rooms[room]):
                protocol.sendLine(message)
