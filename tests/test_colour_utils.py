import unittest

import colourutils as c


class TestColourUtils(unittest.TestCase):
    def test_hex_plain(self):
        self.assertEqual(c.hex_plain(0xF0), 'F0')
        self.assertEqual(c.hex_plain(0xF0F0F0), 'F0F0F0')

    def test_hex_plain_padded(self):
        self.assertEqual(c.hex_plain_padded(0xF0, 6), '0000F0')
        self.assertEqual(c.hex_plain_padded(0xF0F0F0, 6), 'F0F0F0')

    def test_hex_colour_padded(self):
        self.assertEqual(c.hex_colour_padded(0xF0), '0000F0')
        self.assertEqual(c.hex_colour_padded(0xF0F0F0), 'F0F0F0')

    def test_standard_hex_colour_padded(self):
        self.assertEqual(c.standard_hex_colour_padded(0xF0), '0x0000F0')
        self.assertEqual(c.standard_hex_colour_padded(0xF0F0F0), '0xF0F0F0')

    def test_tk_hex_colour_padded(self):
        self.assertEqual(c.tk_hex_colour_padded(0xF0), '#0000F0')
        self.assertEqual(c.tk_hex_colour_padded(0xF0F0F0), '#F0F0F0')

    def test_colour_number_is_valid(self):
        self.assertFalse(c.colour_number_is_valid(0x1000000), 'over max')
        self.assertTrue(c.colour_number_is_valid(0xFFFFFF), 'max')
        self.assertTrue(c.colour_number_is_valid(0x101010), 'nominal')
        self.assertTrue(c.colour_number_is_valid(0), 'min')
        self.assertFalse(c.colour_number_is_valid(-1), 'under min')

    def test_random_colour(self):
        for i in range(10):
            self.assertTrue(0 <= c.random_colour() <= 0xffffff)
