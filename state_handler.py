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

        self.name = name
        self.chats_by_users[name] = self

        self.model = self.session.query(User).filter_by(name=name).first()
        if self.model is None:
            self.model = User(name)
            self.session.add(self.model)
            self.state = 'set_password'
            self.sendLine('Set password for %s' % self.name)
        else:
            self.state = 'check_password'
            self.sendLine('Enter password for %s' % self.name)


        print [user.name for user in self.session.query(User).all()]

    def handle_set_password(self, password):
        self.model.set_password(password)  # TODO: don't store pwd itself, store salted hash
        self.state = 'chat'
        self.sendLine('Registered username %s' % (self.name, ))
        self.sendLine('Welcome, %s!' % (self.name, ))

    def handle_check_password(self, password):
        if self.model.password == password:
            self.state = 'chat'
            self.sendLine('Welcome, %s!' % (self.name, ))
        else:
            self.sendLine('Incorrect password, try again:')

    def handle_chat(self, message):
        message = '<%s> %s' % (self.name, message)
        self.distribute_message(message)