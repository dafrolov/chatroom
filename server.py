import traceback

from sqlalchemy.orm import sessionmaker
from twisted.internet import reactor, task

from db import engine
from chat_factory import ChatFactory


class Server:
    commit_period = 10

    def __init__(self, options):
        self.options = options

        self.session = sessionmaker(bind=engine)()

    def run(self):
        try:
            address = self.options.address
            port = self.options.port

            print 'Starting server on {0}:{1}'.format(address, port)  # TODO: remove prints with logging

            reactor.listenTCP(port, ChatFactory(self.session), interface=address)

            reactor.callWhenRunning(self.commit_loop)

            reactor.run()

        except Exception as e:
            # TODO: add inner level exceptions handling
            print "Server error occurred:".format(e)
            print "Traceback:", traceback.format_exc()

    def commit_loop(self):
        task.LoopingCall(self.session.commit).start(self.commit_period)
