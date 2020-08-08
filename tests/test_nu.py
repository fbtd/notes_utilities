#!/usr/bin/env python3

import unittest
import nu
from collections import namedtuple

TestLines = namedtuple("Testlines", ("name", "original", "enlisted",
                       "enlisted_sorted", "delisted"))

test_lines_list = (
    TestLines("empty", tuple(), list(), list(), tuple()),
    TestLines("simple",("s1", "s3", "s2"),
                [("s1", list()), ("s3", list()), ("s2", list())],
                [("s1", list()), ("s2", list()), ("s3", list())],
            ("s1", "s3", "s2"))
)


class TestNu(unittest.TestCase):

    def test_enlist(self):
        for tl in test_lines_list:
            er = f"failed to enlist {tl.name} TestLines"
            self.assertListEqual(nu.enlist(tl.original), tl.enlisted, er)

if __name__ == '__main__':
    unittest.main()
