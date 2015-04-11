from optparse import OptionParser

from twisted.internet import reactor, stdio, task
from twisted.internet.protocol import Protocol, Factory
from twisted.protocols import basic


class ClientProtocol(Protocol):
    def __init__(self, master):
        self.master = master

    def connectionMade(self):
        task.LoopingCall(self.poll).start(0)

    def poll(self):
        while self.master.input_buffer:
            self.transport.write(
                self.master.input_buffer.pop(0)
            )

    def dataReceived(self, data):
        self.master.output_buffer.append(data.strip('\r\n'))


class ClientFactory(Factory):
    def __init__(self, master):
        self.master = master

    def buildProtocol(self, addr):
        return ClientProtocol(self.master)

    def startedConnecting(self, addr):
        pass

    def clientConnectionLost(self, connector, reason):
        pass

    def clientConnectionFailed(self, _, reason):
        pass


class CommandLineProtocol(basic.LineReceiver):
    delimiter = '\r\n'

    def __init__(self, master):
        self.master = master

    def connectionMade(self):
        self.sendLine('Simple Chat Client v0.1')
        task.LoopingCall(self.poll).start(0)

    def dataReceived(self, line):
        if line:
            self.master.input_buffer.append(line.strip('\n') + '\r\n')

    def poll(self):
        while self.master.output_buffer:
            self.sendLine(self.master.output_buffer.pop(0))


class Client():
    def __init__(self, options):
        self.address = options.address
        self.port = options.port
        self.input_buffer = []
        self.output_buffer = []

    def run(self):
        stdio.StandardIO(CommandLineProtocol(self))
        reactor.connectTCP(self.address, self.port, ClientFactory(self))
        reactor.run()


if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option(
        "-a", "--address",
        dest="address",
        type="str",
        default="127.0.0.1",
        help="Chat client ip address",
    )

    parser.add_option(
        "-p", "--port",
        dest="port",
        type="int",
        default=8123,
        help="Chat client port",
    )

    options, args = parser.parse_args()

    Client(options).run()