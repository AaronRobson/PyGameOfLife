#!/usr/bin/python

import unittest

import gameoflifegui as gui


class TestGameOfLifeGUI(unittest.TestCase):

    def test_GoingToString(self):
        self.assertEqual(gui.GoingToString(False), 'Go')
        self.assertEqual(gui.GoingToString(True), 'Stop')

    def test_BoolToPlusMinusOne(self):
        self.assertEqual(gui.BoolToPlusMinusOne(False), -1)
        self.assertEqual(gui.BoolToPlusMinusOne(True), 1)


if __name__ == "__main__":
    unittest.main()
