import uuid
import hashlib

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
            self.sendLine('Chat session for user %s has been already opened.' % name)
            return

        self.name = name
        self.chats_by_users[name] = self

        self.model = self.session.query(User).filter_by(name=name).first()
        if self.model is None:
            self.model = User(name)
            self.session.add(self.model)
            self.state = 'set_password'
            self.sendLine('Unregistered user %s.' % self.name)
            self.sendLine('Set password for %s to login with this nickname:' % self.name)
        else:
            self.state = 'check_password'
            self.sendLine('Enter password for %s:' % self.name)

        print [user.name for user in self.session.query(User).all()]

    def handle_set_password(self, password):
        user_salt = self.get_salt()
        self.model.set_salt(user_salt)
        user_hash = self.get_salted_hash(password)
        self.model.set_hash(user_hash)

        self.state = 'chat'
        self.sendLine('Registered username %s.' % self.name)
        self.sendLine('You are logged in as %s.' % self.name)

    def handle_check_password(self, password):
        if self.get_salted_hash(password) == self.model.hash:
            self.state = 'chat'
            self.sendLine('You are logged in as %s.' % self.name)
        else:
            self.sendLine('Incorrect password for %s, try again:' % self.name)

    def handle_chat(self, message):
        message = '<%s> %s' % (self.name, message)
        self.distribute_message(message)

    def get_salt(self):
        return uuid.uuid4().hex

    def get_hash(self, value):
        return hashlib.sha512(value).hexdigest()

    def get_salted_hash(self, password):
        h = self.get_hash
        return h(h(password) + self.model.salt)