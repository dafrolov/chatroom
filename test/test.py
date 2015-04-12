import unittest

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
from twisted.internet.task import deferLater

from chat_factory import ChatFactory

from sqlalchemy.orm import sessionmaker
from db import engine


class ClientProtocol(Protocol):
    def __init__(self):
        pass

    def connectionMade(self):
        pass

    def dataReceived(self, data):
        self.output_buffer.append(data)

        if self.input_buffer:
            self.transport.write(self.input_buffer.pop(0) + '\r\n')
        else:
            self.terminate()


class ClientFactory(Factory):
    def __init__(self):
        self.output_buffer = []

    def buildProtocol(self, addr):
        p = ClientProtocol()
        p.output_buffer = self.output_buffer
        p.input_buffer = self.input_buffer
        p.terminate = self.terminate
        return p

    def startedConnecting(self, addr):
        pass

    def clientConnectionLost(self, connector, reason):
        self.terminate()

    def clientConnectionFailed(self, _, reason):
        self.terminate()


class TestChat(unittest.TestCase):
    address = '127.0.0.1'
    port = 8123

    def test_01_login_with_registration(self):
        self.make_server()
        self.set_listener()

        self.make_client()
        self.set_client()
        self.client.input_buffer = [
            'Alice',
            '123456',
        ]

        reactor.run()

        expected = [
            'Login:\r\n',
            'Nickname Alice is free.\r\nSet password for user Alice to register it:\r\n',
            'Registered username Alice.\r\nYou are logged in as Alice.\r\n',
        ]

        self.assertListEqual(self.client.output_buffer, expected)

    def make_server(self):
        session = sessionmaker(bind=engine)()
        self.server = ChatFactory(session)

    def set_listener(self):
        self.listener = reactor.listenTCP(self.port, self.server, interface=self.address)

    def terminate(self):
        deferLater(reactor, 0, self.listener.stopListening) \
            .addCallback(lambda ignored: reactor.crash())

    def make_client(self):
        self.client = ClientFactory()
        self.client.terminate = self.terminate

    def connect(self):
        reactor.connectTCP(self.address, self.port, self.client)

    def set_client(self):
        reactor.callWhenRunning(reactor.callLater, 2, self.connect)
