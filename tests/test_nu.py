#!/usr/bin/env python3

import unittest

from collections import namedtuple
from copy import deepcopy

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import nu

TestLines = namedtuple("Testlines", ("name", "original", "enlisted",
                       "enlisted_sorted", "delisted"))

test_lines_list = (
    TestLines("empty", tuple(), list(), list(), tuple()),
    TestLines("simple",("s1", "s3", "s2"),
                [("s1", list()), ("s3", list()), ("s2", list())],
                [("s1", list()), ("s2", list()), ("s3", list())],
            ("s1", "s3", "s2")),
    TestLines("sub-items",("s1", nu.TAB_CHAR + "ss4", nu.TAB_CHAR + "ss3", "s2"),
                [("s1", [(nu.TAB_CHAR + "ss4", list()),
                         (nu.TAB_CHAR + "ss3", list())]), ("s2", list())],
                [("s1", [(nu.TAB_CHAR + "ss3", list()),
                         (nu.TAB_CHAR + "ss4", list())]), ("s2", list())],
            ("s1", nu.TAB_CHAR + "ss4", nu.TAB_CHAR + "ss3", "s2")),
    TestLines("big-drop",("s1", nu.TAB_CHAR + "ss4", nu.TAB_CHAR *2 + "sss3",
                          "s2"),
                [("s1", [(nu.TAB_CHAR + "ss4", [(nu.TAB_CHAR *2 + "sss3",
                                                list())])]), ("s2", list())],
                [("s1", [(nu.TAB_CHAR + "ss4", [(nu.TAB_CHAR *2 + "sss3",
                                                list())])]), ("s2", list())],
            ("s1", nu.TAB_CHAR + "ss4", nu.TAB_CHAR *2 + "sss3", "s2"))
)

class TestNu(unittest.TestCase):

    def test_helper_get_indent(self):
        self.assertEqual(nu._get_indent("Zero"), 0)
        self.assertEqual(nu._get_indent(nu.TAB_CHAR + "One"), 1)
        self.assertEqual(nu._get_indent(nu.TAB_CHAR *2 + " - Two"), 2)

    def test_enlist(self):
        for tl in test_lines_list:
            er = f"failed to enlist {tl.name} TestLines"
            self.assertListEqual(nu.enlist(tl.original), tl.enlisted, er)

    def test_deepsort(self):
        for tl in test_lines_list:
            tlc = deepcopy(tl)
            nu.deepsort(tlc.enlisted)
            er = f"failed to sort {tl.name} TestLines"
            self.assertListEqual(tlc.enlisted, tl.enlisted_sorted, er)

    def test_delist(self):
        for tl in test_lines_list:
            er = f"failed to delist {tl.name} TestLines"
            self.assertEqual(nu.delist(tl.enlisted), tl.delisted, er)

if __name__ == '__main__':
    unittest.main()
