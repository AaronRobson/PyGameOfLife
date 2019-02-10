#!/usr/bin/python

import unittest

import gameoflife as g


class TestValidateToActualWholeNumber(unittest.TestCase):

    def test_None(self):
        self.assertEqual(g.ValidateToActualWholeNumber(None), 1)

    def test_zero(self):
        self.assertEqual(g.ValidateToActualWholeNumber(0), 1)

    def test_minimum(self):
        self.assertEqual(g.ValidateToActualWholeNumber(1), 1)

    def test_negative(self):
        self.assertEqual(g.ValidateToActualWholeNumber(-3), 1)

    def test_above_minimum(self):
        self.assertEqual(g.ValidateToActualWholeNumber(5), 5)


class TestCheck(unittest.TestCase):

    def test_defaults(self):
        self.assertEqual(g.Check(), [-1, 0, 1])

    def test_off_centre_positive(self):
        self.assertEqual(g.Check(cent=1), [0, 1, 2])

    def test_off_centre_negative(self):
        self.assertEqual(g.Check(cent=-1), [-2, -1, 0])

    def test_zero_range(self):
        self.assertEqual(g.Check(ran=0), [0])

    def test_larger_range(self):
        self.assertEqual(g.Check(ran=2), [-2, -1, 0, 1, 2])

    def test_off_centre_with_larger_range(self):
        self.assertEqual(g.Check(cent=1, ran=2), [-1, 0, 1, 2, 3])


class TestGameOfLife(unittest.TestCase):

    def test_Around(self):
        result = list(g.Around((1, 1, 1)))
        self.assertFalse((1, 1, 1) in result, 'centre cell')
        self.assertTrue((1, 1, 2) in result, 'nominal')
        self.assertTrue((0, 0, 0) in result, 'min')
        self.assertTrue((2, 2, 2) in result, 'max')
        self.assertFalse((3, 1, 1) in result, 'out of range')

    def test_MooreNeighborhood(self):
        result = list(g.MooreNeighborhood((1, 1, 1)))
        self.assertTrue((1, 1, 1) in result, 'centre cell')
        self.assertTrue((1, 1, 2) in result, 'nominal')
        self.assertTrue((0, 0, 0) in result, 'min')
        self.assertTrue((2, 2, 2) in result, 'max')
        self.assertFalse((3, 1, 1) in result, 'out of range')

    def test_AroundList(self):
        aroundListResult = list(g.AroundList((3, 4), (0, 2)))
        expectedResult = [
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (2, 2),
            (2, 3),
            (2, 4),
            (2, 5)]
        self.assertEqual(aroundListResult, expectedResult, '')

    def test_CountAround(self):
        # Glider
        cells = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]

        self.assertEqual(g.CountAround((1, 1), cells), 5, '')
        self.assertEqual(g.CountAround((1, 3), cells), 3, '')
        self.assertEqual(g.CountAround((3, 3), cells), 1, '')
        self.assertEqual(g.CountAround((-1, -1), cells), 0, '')

    def test_AffectableCells(self):
        x = 1
        y = 5
        cells = [(x, y)]
        expected = {
            (x-1, y-1),
            (x-1, y),
            (x-1, y+1),
            (x, y-1),
            (x, y),
            (x, y+1),
            (x+1, y-1),
            (x+1, y),
            (x+1, y+1)}
        self.assertEqual(g.AffectableCells(cells), expected)

    def test_SetCells_Iterate__call__(self):
        exampleKeyList = {(0, 1), (1, 1), (2, 1)}
        gol = g.GameOfLife()
        self.assertEqual(gol(), set())
        gol.cells = exampleKeyList
        self.assertEqual(gol(), exampleKeyList)

        gol.Iterate()
        self.assertEqual(gol(), {(1, 0), (1, 1), (1, 2)})

    def test_FixRange(self):
        self.assertEqual(
            g.FixRange((-1, -1), (0, 0)), ((1, 1), (-1, -1)),
            'minus size')

    def test_RandomBoolean(self):
        possiblities = True, False
        for i in range(10):
            self.assertTrue(g.RandomBoolean() in possiblities)

    def test_population(self):
        gol = g.GameOfLife()
        self.assertEqual(gol.population, 0)
        self.assertEqual(len(gol), 0)

        # Glider
        gol.cells = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]

        self.assertEqual(gol.population, 5)
        self.assertEqual(len(gol), 5)
