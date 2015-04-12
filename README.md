# chatroom
Twisted chat server training example
See https://twistedmatrix.com/documents/13.1.0/core/howto/servers.html

Main dependencies:
- python 2.7.6
- Twisted 14.0.2
- sqlalchemy 0.9.8
- sqlite3


Usage:

- starting server

    $ python run.py -a[address] -p[port]

- starting client

    $ python client.py -a[address] -p[port]

- register new user

    Simple Chat Client v0.1
    Login:
    Alice
    Nickname Alice is free.
    Set password for user Alice to register it:
    123456
    Registered username Alice.
    You are logged in as Alice.

- login existing user

    Simple Chat Client v0.1
    Login:
    Alice
    Enter password for Alice:
    123456
    You are logged in as Alice.

- create a room

    \join_room MyRoom
    You created room MyRoom

- left room

    \left_room MyRoom
    You left room MyRoom 