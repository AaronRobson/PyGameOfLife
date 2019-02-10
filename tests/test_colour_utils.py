import unittest

import colourutils as c


class TestColourUtils(unittest.TestCase):

    def test_HexPlain(self):
        self.assertEqual(c.HexPlain(0xF0), 'F0')
        self.assertEqual(c.HexPlain(0xF0F0F0), 'F0F0F0')

    def test_HexPlainPadded(self):
        self.assertEqual(c.HexPlainPadded(0xF0, 6), '0000F0')
        self.assertEqual(c.HexPlainPadded(0xF0F0F0, 6), 'F0F0F0')

    def test_HexColourPadded(self):
        self.assertEqual(c.HexColourPadded(0xF0), '0000F0')
        self.assertEqual(c.HexColourPadded(0xF0F0F0), 'F0F0F0')

    def test_StandardHexColourPadded(self):
        self.assertEqual(c.StandardHexColourPadded(0xF0), '0x0000F0')
        self.assertEqual(c.StandardHexColourPadded(0xF0F0F0), '0xF0F0F0')

    def test_TKHexColourPadded(self):
        self.assertEqual(c.TKHexColourPadded(0xF0), '#0000F0')
        self.assertEqual(c.TKHexColourPadded(0xF0F0F0), '#F0F0F0')

    def test_ColourNumberIsValid(self):
        self.assertFalse(c.ColourNumberIsValid(0x1000000), 'over max')
        self.assertTrue(c.ColourNumberIsValid(0xFFFFFF), 'max')
        self.assertTrue(c.ColourNumberIsValid(0x101010), 'nominal')
        self.assertTrue(c.ColourNumberIsValid(0), 'min')
        self.assertFalse(c.ColourNumberIsValid(-1), 'under min')
