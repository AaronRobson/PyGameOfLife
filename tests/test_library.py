#!/usr/bin/python

import unittest

import gameoflife as g


class TestCheck(unittest.TestCase):

    def test_defaults(self):
        self.assertEqual(list(g.Check()), [-1, 0, 1])

    def test_off_centre_positive(self):
        self.assertEqual(list(g.Check(cent=1)), [0, 1, 2])

    def test_off_centre_negative(self):
        self.assertEqual(list(g.Check(cent=-1)), [-2, -1, 0])

    def test_zero_range(self):
        self.assertEqual(list(g.Check(ran=0)), [0])

    def test_larger_range(self):
        self.assertEqual(list(g.Check(ran=2)), [-2, -1, 0, 1, 2])

    def test_off_centre_with_larger_range(self):
        self.assertEqual(list(g.Check(cent=1, ran=2)), [-1, 0, 1, 2, 3])


class TestValidateDimensions(unittest.TestCase):

    def test_unpassed_returns_default(self):
        self.assertEqual(g.ValidateDimensions(), g.DEFAULT_NUM_DIMENSIONS)

    def test_explicit_None_returns_default(self):
        self.assertEqual(g.ValidateDimensions(None), g.DEFAULT_NUM_DIMENSIONS)

    def test_valid_number(self):
        self.assertEqual(g.ValidateDimensions(3), 3)

    def test_valid_number_as_string(self):
        self.assertEqual(g.ValidateDimensions('4'), 4)

    def test_TypeError_on_conversion_to_integer_raises_ValueError(self):
        with self.assertRaises(ValueError):
            g.ValidateDimensions(lambda a: a+1)

    def test_ValueError_on_conversion_to_integer_raises_ValueError(self):
        with self.assertRaises(ValueError):
            g.ValidateDimensions('a')

    def test_zero_is_invalid(self):
        with self.assertRaises(ValueError):
            g.ValidateDimensions(0)

    def test_negative_is_invalid(self):
        with self.assertRaises(ValueError):
            g.ValidateDimensions(-1)


class TestAround(unittest.TestCase):

    def setUp(self):
        self.values = list(g.Around((1, 1, 1)))

    def test_centre_cell(self):
        self.assertFalse((1, 1, 1) in self.values)

    def test_within_range(self):
        self.assertTrue((1, 1, 2) in self.values)

    def test_minimum(self):
        self.assertTrue((0, 0, 0) in self.values)

    def test_maximum(self):
        self.assertTrue((2, 2, 2) in self.values)

    def test_out_of_range(self):
        self.assertFalse((3, 1, 1) in self.values)


class TestMooreNeighbourhood(unittest.TestCase):

    def setUp(self):
        self.values = list(g.MooreNeighborhood((1, 1, 1)))

    def test_centre_cell(self):
        self.assertTrue((1, 1, 1) in self.values)

    def test_within_range(self):
        self.assertTrue((1, 1, 2) in self.values)

    def test_minimum(self):
        self.assertTrue((0, 0, 0) in self.values)

    def test_maximum(self):
        self.assertTrue((2, 2, 2) in self.values)

    def test_out_of_range(self):
        self.assertFalse((3, 1, 1) in self.values)


class TestAroundList(unittest.TestCase):

    def test(self):
        actual = list(g.AroundList((3, 4), (0, 2)))
        expected = [
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
            (2, 5),
        ]
        self.assertEqual(actual, expected)


class TestGameOfLife(unittest.TestCase):

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
            self.assertIn(g.RandomBoolean(), possiblities)

    def test_population(self):
        gol = g.GameOfLife()
        self.assertEqual(gol.population, 0)
        self.assertEqual(len(gol), 0)

        # Glider
        gol.cells = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]

        self.assertEqual(gol.population, 5)
        self.assertEqual(len(gol), 5)


class TestCellToChar(unittest.TestCase):

    def test_alive(self):
        self.assertEqual(g.CellToChar(True), 'X')

    def test_dead(self):
        self.assertEqual(g.CellToChar(False), '-')


class TestDisplay(unittest.TestCase):

    def test_glider(self):
        given = [
            [False, True, False],
            [False, False, True],
            [True, True, True],
        ]
        expected = '-X-\n--X\nXXX'
        self.assertEqual(g.Display(given), expected)
