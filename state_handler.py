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
            self.sendLine('Chat session for user %s already opened.' % name)
            return

        self.model = self.session.query(User).filter_by(name=name).first()
        if self.model is None:
            self.model = User(name)
            self.model.set_password('1234556700000')  # TODO: don't store pwd itself, store salted hash
            self.session.add(self.model)

        self.sendLine('Welcome, %s!' % (name, ))
        self.name = name
        self.chats_by_users[name] = self

        self.state = 'chat'

        print [user.name for user in self.session.query(User).all()]

    def handle_get_password(self, password):
        pass

    def handle_chat(self, message):
        message = '<%s> %s' % (self.name, message)
        self.distribute_message(message)