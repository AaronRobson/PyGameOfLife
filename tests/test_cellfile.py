import unittest

from cellfile import line_to_cell, get_cells_from_text


class TestLineToCell(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(list(line_to_cell('')), [])

    def test_comment_only(self):
        self.assertEqual(list(line_to_cell('; example comment')), [])

    def test_pair(self):
        self.assertEqual(list(line_to_cell('1,2')), [1, 2])

    def test_pair_with_comment(self):
        self.assertEqual(list(line_to_cell('3,4; example comment')), [3, 4])


class TestGetCellsFromText(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(get_cells_from_text(''), set())

    def test_realisic(self):
        text = '''; Glider
            1,0
            2,1
            0,2
            1,2
            2,2

            ; R-pentomino
            ; 1,0
            ; 2,0
            ; 0,1
            ; 1,1
            ; 1,2'''
        expected = {
            (1, 0),
            (2, 1),
            (0, 2),
            (1, 2),
            (2, 2),
        }
        self.assertEqual(get_cells_from_text(text), expected)
