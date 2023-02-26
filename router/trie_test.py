import unittest

import trie


class TestCase(unittest.TestCase):
    def test_trie(self):
        t = trie.Tree()
        t.add_router("/user/info", lambda c: c)
        t.add_router("/user/del", lambda c: c)

        self.assertIsNotNone(t.get_handler("/user/del"))


if __name__ == "__main__":
    unittest.main()
