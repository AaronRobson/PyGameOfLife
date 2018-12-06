#!/usr/bin/python

import unittest

import GameOfLife


class TestGameOfLife(unittest.TestCase):
    def setUp(self):
        self.support = GameOfLife
        self.widget = self.support.GameOfLife()

    def test_Around(self):
        result = list(self.support.Around((1, 1, 1)))
        self.assertFalse((1, 1, 1) in result, 'Around Fail: centre cell not being removed from result.')
        self.assertTrue((1, 1, 2) in result, 'Around Fail: not including normal values around centre cell.')
        self.assertTrue((0, 0, 0) in result, 'Around Fail: not including low values around centre cell.')
        self.assertTrue((2, 2, 2) in result, 'Around Fail: not including high values around centre cell.')
        self.assertFalse((3, 1, 1) in result, 'Around Fail: value out of range included.')

    def test_MooreNeighborhood(self):
        result = list(self.support.MooreNeighborhood((1, 1, 1)))
        self.assertTrue((1, 1, 1) in result, 'MooreNeighborhood Fail: centre cell being removed from result.')
        self.assertTrue((1, 1, 2) in result, 'MooreNeighborhood Fail: not including normal values around centre cell.')
        self.assertTrue((0, 0, 0) in result, 'MooreNeighborhood Fail: not including low values around centre cell.')
        self.assertTrue((2, 2, 2) in result, 'MooreNeighborhood Fail: not including high values around centre cell.')
        self.assertFalse((3, 1, 1) in result, 'MooreNeighborhood Fail: value out of range included.')

    def test_AroundList(self):
        aroundListResult = list(self.support.AroundList((3, 4), (0, 2)))
        expectedResult = [(0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (1, 5), (2, 2), (2, 3), (2, 4), (2, 5)]
        self.assertEqual(aroundListResult, expectedResult, '')

    def test_CountAround(self):
        #Glider
        cells = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]

        self.assertEqual(self.support.CountAround((1, 1), cells), 5, '')
        self.assertEqual(self.support.CountAround((1, 3), cells), 3, '')
        self.assertEqual(self.support.CountAround((3, 3), cells), 1, '')
        self.assertEqual(self.support.CountAround((-1, -1), cells), 0, '')

    def test_AffectableCells(self):
        x = 1
        y = 5
        cells = [(x, y)]
        expected = {(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)}
        self.assertEqual(self.support.AffectableCells(cells), expected, 'AffectableCells incorrect.')

    def test_SetCells_Iterate__call__(self):
        exampleKeyList = {(0, 1), (1, 1), (2, 1)}
        self.assertEqual(self.widget(), set(), 'SetCells & __call__ Fail: point listing type or contents incorrect at start.')
        self.widget.cells = exampleKeyList
        self.assertEqual(self.widget(), exampleKeyList, 'SetCells & __call__ Fail: point listing type or contents incorrect after points added.')

        self.widget.Iterate()
        self.assertEqual(self.widget(), {(1, 0), (1, 1), (1, 2)}, 'SetCells & Iterate & __call__ Fail: point listing type or contents incorrect after blinker has one iteration.')

    def test_FixRange(self):
        self.assertEqual(self.support.FixRange((-1, -1), (0, 0)), ((1, 1), (-1, -1)), 'FixRange Fail: incorrectly handles minus size.')

    def test_RandomBoolean(self):
        possiblities = True, False
        for i in range(10):
            self.assertTrue(self.support.RandomBoolean() in possiblities, '')

    def test_population(self):
        self.assertEqual(self.widget.population, 0)
        self.assertEqual(len(self.widget), 0)

        #Glider
        self.widget.cells = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]

        self.assertEqual(self.widget.population, 5)
        self.assertEqual(len(self.widget), 5)


if __name__ == "__main__":
    unittest.main()
