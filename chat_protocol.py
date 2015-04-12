from twisted.protocols.basic import LineReceiver

from command_handler import CommandHandler
from state_handler import StateHandler
from db.message import Message
from db.room import Room


class ChatProtocol(LineReceiver, StateHandler, CommandHandler):

    def __init__(self, master):
        self.session = master.session
        self.chats_by_users = master.chats_by_users
        self.users_by_rooms = master.users_by_rooms

        self.name = None
        self.state = 'get_name'

    def connectionMade(self):
        self.sendLine("Login:")

    def connectionLost(self, reason):
        if self.name in self.chats_by_users:
            del self.chats_by_users[self.name]

    def lineReceived(self, line):
        if self.state == 'chat' and line.startswith('\\'):
            line = line.lstrip('\\')
            self.handle_command(line)
        else:
            self.handle_state(line)

    def distribute_message(self, message, room=None):
        collocutors = self.collocutors_by_room(room) if room else self.all_collocutors

        if not collocutors:
            self.sendLine("Nobody could hear you.")
            if not self.rooms:
                self.sendLine("Please, create or enter a chat room.")
            else:
                self.sendLine("Please, wait for collocutors.")

        for user in collocutors:
            self.chats_by_users[user].sendLine(message)

        message_model = Message(self.model.id, message)
        message_model.rooms = self.session.query(Room).filter(Room.name.in_([room] if room else self.rooms)).all()
        self.session.add(message_model)

    def collocutors_by_room(self, room):
        return set(self.users_by_rooms[room]) - set([self.name])

    @property
    def all_collocutors(self):
        selected_users = [users for users in self.users_by_rooms.itervalues() if self.name in users]
        return reduce(set.union, map(set, selected_users), set()) - set([self.name])

    @property
    def rooms(self):
        return [room for room, users in self.users_by_rooms.iteritems() if self.name in users]