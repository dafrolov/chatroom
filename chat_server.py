"""
    Taken from Twisted documentation
    https://twistedmatrix.com/documents/13.1.0/core/howto/servers.html
"""
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor


class StateHandler():

    def handle_state(self, line):
        try:
            method = getattr(self, 'handle_' + self.state)
        except AttributeError:
            pass
        else:
            result = method(line)

    def handle_get_name(self, name):
        if name in self.chats_by_users:
            self.sendLine('Name taken, please choose another.')
            return

        self.sendLine('Welcome, %s!' % (name, ))
        self.name = name
        self.chats_by_users[name] = self
        self.state = 'chat'

    def handle_get_password(self, password):
        pass

    def handle_chat(self, message):  # TODO: lowercase state names
        message = '<%s> %s' % (self.name, message)
        self.distribute_message(message)


class CommandHandler():

    def handle_command(self, line):
        try:
            command, params = line.split(' ', 1)
        except ValueError:
            self.sendLine('Invalid command format: "%s"' % line)
            return

        try:
            method = getattr(self, 'handle_' + command)  # TODO: method_by_command_name
        except AttributeError:
            self.sendLine('Unknown command: %s' % command)
            return
        else:
            result = method(params)

    def handle_join_room(self, room):
        if room not in self.users_by_rooms:
            self.users_by_rooms[room] = [self.name]
            self.sendLine('You created room %s' % room)

        elif self.name in self.users_by_rooms[room]:
            self.sendLine('Already in room %s' % room)

        else:
            self.users_by_rooms[room].append(self.name)
            self.sendLine('You joined room %s' % room)
            self.distribute_message('User %s joined room %s' % (self.name, room), room)

        print self.users_by_rooms

    def handle_left_room(self, room):
        if room not in self.users_by_rooms:
            self.sendLine('Room %s does not exist' % room)

        elif self.name in self.users_by_rooms[room]:
            self.users_by_rooms[room].remove(self.name)
            self.sendLine('You left room %s ' % room)
            self.distribute_message('User %s left room %s' % (self.name, room), room)

        else:
            self.sendLine('You are not in room %s ' % room)

        print self.users_by_rooms


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


class ChatFactory(Factory):

    def __init__(self):
        self.chats_by_users = {}
        self.users_by_rooms = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)


reactor.listenTCP(8123, ChatFactory())  # TODO separate starter with optparse
reactor.run()
