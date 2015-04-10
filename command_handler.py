

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
