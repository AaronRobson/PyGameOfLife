from typing import Iterable, Optional, Set, Tuple
from random import randrange
from itertools import product
from rule import Rule

Cell = Tuple[int, ...]
Cells = Set[Cell]

_todo: str = '''To-Do:
Have a boolean flag isStatic which is reset when change is made to the cells,
so that it knows it doesn't have to change anything for the next generation.

Be able to initialise with a tuple/set of tuples live cells, in order
to continue from some defined state such as the last time it was run.
'''

'''
-X-
--X
XXX
'''
glider: Cells = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}
glider_period: int = 4

gosper_glider_gun: Cells = {
    (0, 6), (0, 7), (1, 6), (1, 7),  # block
    (8, 7), (8, 8), (9, 6), (9, 8), (10, 6), (10, 7),  # beehive
    (16, 8), (16, 9), (16, 10), (17, 8), (18, 9),  # glider
    (22, 5), (22, 6), (23, 4), (23, 6), (24, 4), (24, 5),  # beehive
    (34, 4), (34, 5), (35, 4), (35, 5),  # block
    (24, 16), (24, 17), (25, 16), (25, 18), (26, 16),  # glider
    (35, 11), (35, 12), (35, 13), (36, 11), (37, 12),  # gliders
}

default_size: int = 50

# For co-ordinates.
origin: int = 0


def check(cent: int = 0, ran: int = 1) -> Iterable[int]:
    '''Defaults make = [-1,0,1]
    '''
    cent = int(cent)
    ran = abs(int(ran))
    return range(cent - ran, 1 + cent + ran)


# Must be an integer; 1 or above
default_num_dimensions: int = 2
validate_dimensions_error: str = 'Dimensions must be an integer of at least 1.'


def validate_dimensions(dimensions: Optional[int] = None) -> int:
    '''May raise ValueError exception.
    '''
    if dimensions is None:
        dimensions = default_num_dimensions

    try:
        dimensions = int(dimensions)
    except (ValueError, TypeError):
        raise ValueError(validate_dimensions_error)
    else:
        # No such thing as negative or 0 dimensions this side of Event Horizon.
        if 1 <= dimensions:
            return dimensions
        else:
            raise ValueError(validate_dimensions_error)


def random_boolean() -> bool:
    '''Choice of True or False enforced from a choice of 1 or 0.
    '''
    return bool(randrange(2))


def count_around(cell: Cell, cells: Cells) -> int:
    '''Add up all the present has_keys for all those Around()
    a given cell in the 'Current Array'.
    '''
    return sum(p in cells for p in around(cell))


def moore_neighborhood(origin: Cell) -> Cells:
    '''Like AroundList but can take advantage of the fact that check
    [-1,0,1] is the same for all dimensions.
    '''
    dimension_values = map(check, origin)
    return set(product(*dimension_values))


def around(origin: Cell) -> Cells:
    return set(filter(lambda x: x != origin, moore_neighborhood(origin)))


def around_list(size: int, origin: Cell) -> Iterable[Cell]:
    '''Returns tuples of co-ordinates for a given range.
    Built from ideas learned on the making of Around().
    '''
    def low_high(size, origin):
        return range(origin, origin + size)

    # http://www.daniweb.com/software-development/python/threads/272931

    dimensional_ranges = map(low_high, *fix_range(size, origin))
    return product(*dimensional_ranges)


def fix_range(size, origin):
    '''If a dimension is a minus size it it converted to positive
    and the origin is adjusted to compensate.
    This is done for all dimensions together.
    '''
    def fix(size_dim, origin_dim):
        if size_dim < 0:
            size_dim = -size_dim
            origin_dim -= size_dim
        return size_dim, origin_dim

    """The zip should truncate the values to the smallest of
    the two in length (only applicable if they have different
    numbers of dimensions, which they should not)."""
    return tuple(zip(*map(fix, size, origin)))


def will_be_alive(cell, cells, rule: Rule) -> bool:
    '''Will a given cell be alive in the next generation?
    '''
    return rule.is_alive_next_generation(
        cell in cells,
        count_around(cell, cells))


def affectable_cells(cells: Cells) -> Cells:
    '''All the live cells and all those around them within
    range of checking without duplicates.
    '''
    return {c for cell in cells for c in moore_neighborhood(cell)}


def cells_of_next_generation(cells: Cells, rule: Rule) -> Cells:
    return {cell
            for cell in affectable_cells(cells)
            if will_be_alive(cell, cells, rule)}


class GameOfLife():
    def __init__(self, dim=None, rule_str=None):
        '''"dim" is the number of dimensions wanted and the ruleStr is a string
        consisting of two sets of an arbitary number of integer values
        separated with a '/' (forward slash).

        The first set refers to the allowed numbers of live cells around each
        live cell that will make it stay alive, the second refers to how many
        needed to make a new cell be born.

        These numbers may but have no obligation to overlap.
        '''
        self.dimensions = validate_dimensions(dim)

        self.rule = Rule(rule_str)

        self.reset()

    def reset(self) -> None:
        '''Default view size, position, statistics and cells.
        '''
        self.size: int = default_size

        """Population <=1/2 of maximum population for a stable arrangement,
        this favours a sparse data storage choice.
        """
        self.cells: Cells = set()

    def iterate(self) -> None:
        '''Do a single iteration.
        '''
        self.cells = cells_of_next_generation(self.cells, self.rule)

    def random(self, size=None, origin=None):
        '''A minus size will just select in the other direction.
        Has to be limited so it doesn't try to assign a value to
        every coordinate in infinity.
        '''
        if size is None:
            size = (self.size,) * self.dimensions

        if origin is None:
            origin = (self.origin,) * self.dimensions

        for cell in around_list(*fix_range(size, origin)):
            self.set_cell(cell, random_boolean())

    def is_cell_alive(self, cell: Cell) -> bool:
        return cell in self.cells

    def toggle_cell(self, cell: Cell) -> None:
        self.set_cell(cell, not self.is_cell_alive(cell))

    def set_cell(self, cell: Cell, value: Optional[bool] = True) -> None:
        if value:
            self.cells.add(cell)
        else:
            self.cells.discard(cell)

    def get_range(self, size=None, origin=None) -> Iterable[Iterable[bool]]:
        '''A minus size will just select in the other direction. Assumes 2D.
        '''
        if not size:
            size = (self.size,) * self.dimensions

        if not origin:
            origin = (origin,) * self.dimensions

        size, origin = fix_range(size, origin)

        ranges = around_list(size, origin)

        # depends upon number of dimensions and how AroundList is sorted
        dimension_wrap_on = 1

        line_place = origin[dimension_wrap_on] + size[dimension_wrap_on]

        grid = []
        line = []
        for r in ranges:
            line.append(r in self.cells)
            # Is the end of a line?
            if r[dimension_wrap_on] == line_place - 1:
                grid.append(line)
                line = []
        return grid

    @property
    def population(self) -> int:
        '''As a side effect of storing co-ordinates as a sparse dataset,
        population does not have to be counted by exhaustive searching.
        '''
        return len(self.cells)

    @property
    def rule(self) -> Rule:
        return self._rule

    @rule.setter
    def rule(self, rule: Rule) -> None:
        self._rule = rule

    @property
    def rule_str(self) -> str:
        return str(self.rule)

    @rule_str.setter
    def rule_str(self, rule_str: str) -> None:
        self.rule = Rule(rule_str)

    @property
    def cells(self) -> Cells:
        return self._cells

    @cells.setter
    def cells(self, cells: Cells) -> None:
        self._cells = set(cells)

    def __len__(self) -> int:
        return self.population


def cell_to_char(cell_val: bool) -> str:
    return 'X' if cell_val else '-'


def display(grid: Iterable[Iterable[bool]]) -> str:
    '''Because of the dimensional limitations of the display,
    only 2 dimensions can be handled in this manner
    (or one if given in the 2d format).
    '''
    return '\n'.join(
        [''.join(
            [cell_to_char(cell) for cell in line]
        ) for line in grid]
    )


def main() -> None:
    print('Game Of Life - Testing')

    gol = GameOfLife()

    gol.cells = glider
    # gol.cells = gosper_glider_gun

    for r in range(-1, glider_period):
        '''Display every time including when r == -1 but only Iterate() from 0,
        so that the initial state is shown on screen.'''
        if not r < 0:
            gol.iterate()
        print()  # separate the displays
        print(display(gol.get_range(size=(5, 5), origin=(0, 0))))

    print('\nPopulation: ' + str(gol.population))

    print(repr(gol.rule))


if __name__ == "__main__":
    main()
