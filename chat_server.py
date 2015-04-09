"""
    Taken from Twisted documentation
    https://twistedmatrix.com/documents/13.1.0/core/howto/servers.html
"""
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor


class ChatProtocol(LineReceiver):

    def __init__(self, master):
        self.chats_by_users = master.chats_by_users
        self.users_by_rooms = master.users_by_rooms

        self.name = None
        self.state = 'GETNAME'

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

    def handle_state(self, line):  # TODO: StateHandler
        try:
            method = getattr(self, 'handle_state_' + self.state)
        except AttributeError:
            pass
        else:
            result = method(line)

    def handle_command(self, line):  # TODO: CommandHandler
        try:
            command, params = line.split(' ', 1)
        except ValueError:
            self.sendLine('Invalid command format: "%s"' % line)
            return

        try:
            method = getattr(self, 'handle_command_' + command)  # TODO: method_by_command_name
        except AttributeError:
            self.sendLine('Unknown command: %s' % command)
            return
        else:
            result = method(params)

    def handle_state_GETNAME(self, name):
        if name in self.chats_by_users:
            self.sendLine('Name taken, please choose another.')
            return

        self.sendLine('Welcome, %s!' % (name, ))
        self.name = name
        self.chats_by_users[name] = self
        self.state = 'CHAT'

    def handle_state_GETPASSWORD(self, password):
        pass

    def handle_state_CHAT(self, message):  # TODO: lowercase state names
        message = '<%s> %s' % (self.name, message)
        for name, protocol in self.chats_by_users.iteritems():
            if protocol != self:
                protocol.sendLine(message)

    def handle_command_join_room(self, room):
        if room not in self.users_by_rooms:
            self.users_by_rooms[room] = [self.name]
            self.sendLine('You created room %s' % room)

        elif self.name in self.users_by_rooms[room]:
            self.sendLine('Already in room %s' % room)

        else:
            self.users_by_rooms[room].append(self.name)
            self.sendLine('You joined room %s' % room)
            # TODO: inform other users

        print self.users_by_rooms

    def handle_command_left_room(self, room):
        if room not in self.users_by_rooms:
            self.sendLine('Room %s does not exist' % room)

        elif self.name in self.users_by_rooms[room]:
            self.users_by_rooms[room].remove(self.name)
            self.sendLine('You left room %s ' % room)
            # TODO: inform other users

        else:
            self.sendLine('You are not in room %s ' % room)

        print self.users_by_rooms


class ChatFactory(Factory):

    def __init__(self):
        self.chats_by_users = {}
        self.users_by_rooms = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)


reactor.listenTCP(8123, ChatFactory())  # TODO separate starter with optparse
reactor.run()
