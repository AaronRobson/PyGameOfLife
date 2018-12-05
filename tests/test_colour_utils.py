import unittest

import colourutils


class TestColourUtils(unittest.TestCase):

    def setUp(self):
        self.support = colourutils

    def test_HexPlain(self):
        self.assertEqual(self.support.HexPlain(0xF0), 'F0', '')
        self.assertEqual(self.support.HexPlain(0xF0F0F0), 'F0F0F0', '')

    def test_HexPlainPadded(self):
        self.assertEqual(self.support.HexPlainPadded(0xF0, 6), '0000F0', '')
        self.assertEqual(self.support.HexPlainPadded(0xF0F0F0, 6), 'F0F0F0', '')

    def test_HexColourPadded(self):
        self.assertEqual(self.support.HexColourPadded(0xF0), '0000F0', '')
        self.assertEqual(self.support.HexColourPadded(0xF0F0F0), 'F0F0F0', '')

    def test_StandardHexColourPadded(self):
        self.assertEqual(self.support.StandardHexColourPadded(0xF0), '0x0000F0', '')
        self.assertEqual(self.support.StandardHexColourPadded(0xF0F0F0), '0xF0F0F0', '')

    def test_TKHexColourPadded(self):
        self.assertEqual(self.support.TKHexColourPadded(0xF0), '#0000F0', '')
        self.assertEqual(self.support.TKHexColourPadded(0xF0F0F0), '#F0F0F0', '')

    def test_ColourNumberIsValid(self):
        self.assertFalse(self.support.ColourNumberIsValid(0x1000000), 'Outside lower limit.')
        self.assertTrue(self.support.ColourNumberIsValid(0xFFFFFF), 'Within lower limit')
        self.assertTrue(self.support.ColourNumberIsValid(0x101010), 'Nominal.')
        self.assertTrue(self.support.ColourNumberIsValid(0), 'Within upper limit.')
        self.assertFalse(self.support.ColourNumberIsValid(-1), 'Outside upper limit.')


if __name__ == "__main__":
    unittest.main()
