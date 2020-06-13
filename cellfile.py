from typing import Iterable
from gameoflife import Cell, Cells


# file options
file_cell_splitter = '\n'
file_cell_dimension_splitter = ','
file_cell_comment = ';'


def get_file_text(filepath: str) -> str:
    '''Get contents of file.
    Assumes contents are small enough to read in all together without problems.
    If the file does not exist will raise IOError exception
    '''
    with open(filepath, 'r') as f:
        return f.read()


def remove_comments(line: str) -> str:
    return line.split(file_cell_comment)[0].strip()


def line_to_cell(line: str) -> Cell:
    line = remove_comments(line)
    if line:
        return tuple(map(int, line.split(file_cell_dimension_splitter)))
    else:
        return ()


def cell_to_line(cell: Cell) -> str:
    return file_cell_dimension_splitter.join(map(str, cell))


def cells_to_lines(cells: Cells) -> Iterable[str]:
    return map(cell_to_line, sorted(cells))


def get_cells_from_text(text: str) -> Cells:
    cells = set()
    for line in text.split(file_cell_splitter):
        cell = tuple(line_to_cell(line))
        if cell:
            cells.add(cell)
    return cells


def load(filepath: str) -> Cells:
    return get_cells_from_text(get_file_text(filepath))


def save(filepath: str, cells: Cells) -> None:
    with open(filepath, 'w') as f:
        for line in cells_to_lines(cells):
            f.write(line + file_cell_splitter)
