# file options
file_cell_splitter = '\n'
file_cell_dimension_splitter = ','
file_cell_comment = ';'


def get_file_text(filepath):
    '''Get contents of file.
    Assumes contents are small enough to read in all together without problems.
    If the file does not exist will raise IOError exception
    '''
    with open(filepath, 'r') as f:
        return f.read()


def remove_comments(line):
    return line.split(file_cell_comment)[0].strip()


def line_to_cell(line):
    line = remove_comments(line)
    if line:
        return map(int, line.split(file_cell_dimension_splitter))
    else:
        return ()


def get_cells_from_text(text):
    cells = set()
    for line in text.split(file_cell_splitter):
        cell = tuple(line_to_cell(line))
        if cell:
            cells.add(cell)
    return cells


def get_cells_from_file(filepath):
    return get_cells_from_text(get_file_text(filepath))
