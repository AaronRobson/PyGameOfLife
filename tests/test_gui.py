import unittest

import gameoflifegui as gui


class TestColourTypeToString(unittest.TestCase):

    def test_foreground(self):
        self.assertEqual(gui.colour_type_to_string(True), 'Foreground')

    def test_background(self):
        self.assertEqual(gui.colour_type_to_string(False), 'Background')


class TestColourTypeToChangeString(unittest.TestCase):

    def test_foreground(self):
        self.assertEqual(
            gui.colour_type_to_change_string(True),
            'Change Foreground')

    def test_background(self):
        self.assertEqual(
            gui.colour_type_to_change_string(False),
            'Change Background')


class TestGameOfLifeGUI(unittest.TestCase):

    def test_going_to_sring(self):
        self.assertEqual(gui.going_to_string(False), 'Go')
        self.assertEqual(gui.going_to_string(True), 'Stop')

    def test_bool_to_plus_minus_one(self):
        self.assertEqual(gui.bool_to_plus_minus_one(False), -1)
        self.assertEqual(gui.bool_to_plus_minus_one(True), 1)
