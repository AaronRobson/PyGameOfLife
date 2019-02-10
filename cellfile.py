#!/usr/bin/python

# file options
fileCellSplitter = '\n'
fileCellDimensionSplitter = ','
fileCellComment = ';'


def GetFileText(filepath):
    '''Get contents of file.
    Assumes contents are small enough to read in all together without problems.
    If the file does not exist will raise IOError exception
    '''
    with open(filepath, 'r') as f:
        return f.read()


def RemoveComments(line):
    return line.split(fileCellComment)[0].strip()


def LineToCell(line):
    line = RemoveComments(line)
    if line:
        return map(int, line.split(fileCellDimensionSplitter))
    else:
        return ()


def GetCellsFromText(text):
    for line in text.split(fileCellSplitter):
        cell = tuple(LineToCell(line))
        if cell:
            yield cell


def GetCellsFromFile(filepath):
    return GetCellsFromText(GetFileText(filepath))
