#!/usr/bin/python

import unittest

import GameOfLifeGUI


class TestGameOfLifeGUI(unittest.TestCase):

    def setUp(self):
        self.support = GameOfLifeGUI

    def test_GoingToString(self):
       self.assertEqual(self.support.GoingToString(False), 'Go')
       self.assertEqual(self.support.GoingToString(True), 'Stop')

    def test_BoolToPlusMinusOne(self):
      self.assertEqual(self.support.BoolToPlusMinusOne(False), -1)
      self.assertEqual(self.support.BoolToPlusMinusOne(True), 1)


if __name__ == "__main__":
    unittest.main()
