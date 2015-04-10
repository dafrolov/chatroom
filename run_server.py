from twisted.internet import reactor

from chat_factory import ChatFactory


if __name__ == "__main__":
    # TODO optparse
    reactor.listenTCP(8123, ChatFactory())
    reactor.run()
