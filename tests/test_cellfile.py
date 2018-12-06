import unittest

import cellfile


class TestLineToCell(unittest.TestCase):

    def test(self):
        self.assertEqual(cellfile.LineToCell('1,2'), [1, 2])


if __name__ == "__main__":
    unittest.main()
