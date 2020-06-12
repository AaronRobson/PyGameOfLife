import unittest

import gameoflife as g


class TestCheck(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(list(g.check()), [-1, 0, 1])

    def test_off_centre_positive(self):
        self.assertEqual(list(g.check(cent=1)), [0, 1, 2])

    def test_off_centre_negative(self):
        self.assertEqual(list(g.check(cent=-1)), [-2, -1, 0])

    def test_zero_range(self):
        self.assertEqual(list(g.check(ran=0)), [0])

    def test_larger_range(self):
        self.assertEqual(list(g.check(ran=2)), [-2, -1, 0, 1, 2])

    def test_off_centre_with_larger_range(self):
        self.assertEqual(list(g.check(cent=1, ran=2)), [-1, 0, 1, 2, 3])


class TestValidateDimensions(unittest.TestCase):
    def test_unpassed_returns_default(self):
        self.assertEqual(g.validate_dimensions(), g.default_num_dimensions)

    def test_explicit_none_returns_default(self):
        self.assertEqual(g.validate_dimensions(None), g.default_num_dimensions)

    def test_valid_number(self):
        self.assertEqual(g.validate_dimensions(3), 3)

    def test_valid_number_as_string(self):
        self.assertEqual(g.validate_dimensions('4'), 4)

    def test_type_error_on_conversion_to_integer_raises_value_error(self):
        with self.assertRaises(ValueError):
            g.validate_dimensions(lambda a: a+1)

    def test_value_error_on_conversion_to_integer_raises_value_error(self):
        with self.assertRaises(ValueError):
            g.validate_dimensions('a')

    def test_zero_is_invalid(self):
        with self.assertRaises(ValueError):
            g.validate_dimensions(0)

    def test_negative_is_invalid(self):
        with self.assertRaises(ValueError):
            g.validate_dimensions(-1)


class TestAround(unittest.TestCase):
    def setUp(self):
        self.values = list(g.around((1, 1, 1)))

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
        self.values = g.moore_neighborhood((1, 1, 1))

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
        actual = g.around_list((3, 4), (0, 2))
        expected = {
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
        }
        self.assertEqual(actual, expected)

    def test_3d(self):
        actual = g.around_list((2, 2, 2), (1, 1, 1))
        expected = {
            (1, 1, 1),
            (1, 1, 2),
            (1, 2, 1),
            (1, 2, 2),
            (2, 1, 1),
            (2, 1, 2),
            (2, 2, 1),
            (2, 2, 2),
        }
        self.assertEqual(actual, expected)


class TestGameOfLife(unittest.TestCase):
    def test_count_around(self):
        # Glider
        cells = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]

        self.assertEqual(g.count_around((1, 1), cells), 5, '')
        self.assertEqual(g.count_around((1, 3), cells), 3, '')
        self.assertEqual(g.count_around((3, 3), cells), 1, '')
        self.assertEqual(g.count_around((-1, -1), cells), 0, '')

    def test_affectable_cells(self):
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
        self.assertEqual(g.affectable_cells(cells), expected)

    def test_set_cells_iterate__call__(self):
        given_keys = {(0, 1), (1, 1), (2, 1)}
        gol = g.GameOfLife()
        self.assertEqual(gol(), set())
        gol.cells = given_keys
        self.assertEqual(gol(), given_keys)

        gol.iterate()
        self.assertEqual(gol(), {(1, 0), (1, 1), (1, 2)})

    def test_set_cell(self):
        given_cell = (1, 2)
        gol = g.GameOfLife()
        gol.set_cell(given_cell, True)
        self.assertEqual(gol.cells, {given_cell})
        gol.set_cell(given_cell, False)
        self.assertEqual(gol.cells, set())
        gol.set_cell(given_cell, False)
        self.assertEqual(gol.cells, set())

    def test_fix_range(self):
        self.assertEqual(
            g.fix_range((-1, -1), (0, 0)), ((1, 1), (-1, -1)),
            'minus size')

    def test_random_boolean(self):
        possiblities = True, False
        for i in range(10):
            self.assertIn(g.random_boolean(), possiblities)

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
        self.assertEqual(g.cell_to_char(True), 'X')

    def test_dead(self):
        self.assertEqual(g.cell_to_char(False), '-')


class TestDisplay(unittest.TestCase):
    def test_glider(self):
        given = [
            [False, True, False],
            [False, False, True],
            [True, True, True],
        ]
        expected = '-X-\n--X\nXXX'
        self.assertEqual(g.display(given), expected)
