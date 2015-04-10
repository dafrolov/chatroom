from db.user import User


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

        self.model = User(name)
        self.model.set_password('1234556700000')
        self.session.add(self.model)

        print self.session.query(User).first()
        #self.session.commit()


    def handle_get_password(self, password):
        pass

    def handle_chat(self, message):
        message = '<%s> %s' % (self.name, message)
        self.distribute_message(message)