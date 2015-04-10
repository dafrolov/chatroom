from twisted.internet import reactor

from chat_factory import ChatFactory

import db


if __name__ == "__main__":
    # TODO optparse
    factory = ChatFactory()
    reactor.listenTCP(8123, factory)
    reactor.callLater(5, factory.startCommitLoop)
    reactor.run()
