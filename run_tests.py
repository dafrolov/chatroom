import unittest
import sys

import config
config.testing = True


def main():
    suite = unittest.TestLoader().discover('./test')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    no_errors = len(result.errors) + len(result.failures) == 0
    sys.exit(0 if no_errors else 1)


if __name__ == '__main__':
    main()