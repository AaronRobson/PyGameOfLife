import unittest

import cellfile


class TestLineToCell(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(list(cellfile.LineToCell('')), [])

    def test_comment_only(self):
        self.assertEqual(list(cellfile.LineToCell('; example comment')), [])

    def test_pair(self):
        self.assertEqual(list(cellfile.LineToCell('1,2')), [1, 2])

    def test_pair_with_comment(self):
        self.assertEqual(list(cellfile.LineToCell('3,4; example comment')), [3, 4])
