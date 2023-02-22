import unittest
from http import server

import engine


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here
        s = server.HTTPServer(("", 8000), server.SimpleHTTPRequestHandler)
        s.serve_forever()


def test_for_normal_routine():
    r = engine.Engine()
    r.add_route("/ping", lambda c: print(c), "GET")  # add a get route
    r.run_server()


if __name__ == '__main__':
    # unittest.main()
    test_for_normal_routine()
