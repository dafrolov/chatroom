# chatroom
Twisted chat server training example
See https://twistedmatrix.com/documents/13.1.0/core/howto/servers.html

Main dependencies:
- python 2.7.6
- Twisted 14.0.2


Usage:

- starting server

    $ python chat_server.py

- communicate with telnet

    $ telnet 127.0.0.1 8123
    Trying 127.0.0.1...
    Connected to 127.0.0.1.
    Escape character is '^]'.
    What's your name?
    test
    Name taken, please choose another.
    bob
    Welcome, bob!
    hello
    <alice> hi bob
    twisted makes writing servers so easy!
    <alice> I couldn't agree more
    <carrol> yeah, it's great