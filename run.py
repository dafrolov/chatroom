from optparse import OptionParser

from server import Server


if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option(
        "-a", "--address",
        dest="address",
        type="str",
        default="127.0.0.1",
        help="Chat server ip address",
    )

    parser.add_option(
        "-p", "--port",
        dest="port",
        type="int",
        default=8123,
        help="Chat server port",
    )

    options, args = parser.parse_args()

    Server(options).run()
