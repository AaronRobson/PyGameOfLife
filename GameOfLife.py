#!/usr/bin/python

from random import randrange
from string import digits
from functools import reduce
from operator import mul as OpMultiply
from itertools import product as itertoolsProduct
from counter import Counter

_todo = '''To-Do:

Make game stop when the iteration is the same as the last.

Have a boolean flag isStatic which is reset when change is made to the cells,
so that it knows it doesn't have to change anything for the next generation.

Be able to initialise with a tuple/set of tuples live cells, in order
to continue from some defined state such as the last time it was run.

'''

STRING_RULE_SEPARATOR = '/'
#'3/23'
CONWAY_STANDARD_STRING_RULE = STRING_RULE_SEPARATOR.join(['3', '23'])

DEFAULT_SIZE = 50
DEFAULT_ORIGIN = 0

def ProductOfSeq(seq):
  return reduce(OpMultiply, seq)

def ValidateToActualWholeNumber(num):
  '''No negative, fractional or zero numbers.
  '''
  default = 1
  try:
    number = int(number)
  except (ValueError, TypeError):
    return default
  else:
    if default < number:
      return number
    else:
      return default

class Rule():
  def __init__(self, ruleStr=None):
    self._rule = self._StringToRule(ruleStr)

  @property
  def string(self):
    return self._RuleToString(self._rule)

  def IsAliveNextGeneration(self, aliveNow, liveCellsAround):
    aliveNow = bool(aliveNow)
    return liveCellsAround in self._rule[aliveNow]

  def __str__(self):
    return self.string

  def __repr__(self):
    return '%s(%r)' % (self.__class__.__name__, self.string)

  def __call__(self):
    return self.string

  def _StringToDigitTuple(self, digitString):
    '''Sorts and removes duplicates.
    Returns the canonical representation.
    '''
    return tuple(sorted(set(int(char) for char in digitString if str(char) in digits)))

  def _RuleToString(self, rule):
    '''Returns the string notation of an inputted rule data structure,
    Exactly opposite to StringToRule when using valid notations.
    '''

    #outer one uses a direct list as join takes longer to deal with generator objects
    return STRING_RULE_SEPARATOR.join([
          #inner one makes a generator object rather than a list directly, speeds up 
          ''.join((str(int(num)) for num in subList))
        for subList in rule[:2]
    ])

  def _StringToRule(self, stringRule=None):
    '''Returns the rule data structure of an inputted string notation.
    If no string is specified the John Conway standard rule string is used
    Exactly opposite to StringToRule when using valid notations.
    '''
    if stringRule is None: stringRule = CONWAY_STANDARD_STRING_RULE

    splitRules = stringRule.split(STRING_RULE_SEPARATOR)

    #All after the second '/' if present is ignored
    output = [()]*2
    count = min(len(output), len(splitRules))
    for s in range(count):
      #if char not in string .digits ignore it as bad value and move on
      output[s] = self._StringToDigitTuple(splitRules[s])
    return tuple(output)

def Check(cent=0, ran=1):
  '''Defaults make = [-1,0,1]
  '''
  cent = int(cent)
  ran = abs(int(ran))
  return range(cent - ran, 1 + cent + ran)

#Must be an integer; 1 or above
DEFAULT_NUM_DIMENSIONS = 2
VALIDATE_DIMENSIONS_ERROR = 'Dimensions must be an integer of at least 1.'
def ValidateDimensions(dimensions=None):
  '''May raise ValueError exception.
  '''
  if dimensions is None:
    dimensions = DEFAULT_NUM_DIMENSIONS

  try:
    dimensions = int(dimensions)
  except (ValueError, TypeError):
    raise ValueError(VALIDATE_DIMENSIONS_ERROR)
  else:
    #No such thing as negative or 0 dimensions this side of Event Horizon.
    if 1 <= dimensions:
      return dimensions
    else:
      raise ValueError(VALIDATE_DIMENSIONS_ERROR)

def RandomBoolean():
  '''Choice of True or False enforced from a choice of 1 or 0.
  '''
  return bool(randrange(2))

class GameOfLife():
  def __init__(self, *args, **kwargs):
    '''"dim" is the number of dimensions wanted and the ruleStr is a string
    consisting of two sets of an arbitary number of integer values separated 
    with a '/' (forward slash).
    
    The first set refers to the allowed numbers of live cells around each
    live cell that will make it stay alive, the second refers to how many
    needed to make a new cell be born.
    
    These numbers may but have no obligation to overlap.
    '''
    self.Restart(*args, **kwargs)

  def Restart(self, dim=None, ruleStr=None):
    '''As if the class had been destroyed and a new one created.
    '''
    self.dimensions = ValidateDimensions(dim)

    #run at every place at which it may need to be changed
    self._check = tuple(Check())

    self._currRule = Rule(ruleStr)

    self.Reset()

  def Reset(self):
    '''Default view size, position, statistics and cells.
    '''
    self.SIZE = DEFAULT_SIZE
    self.ORIGIN = DEFAULT_ORIGIN

    self._generation = Counter()

    """Population <=1/2 of maximum population for a stable arrangement,
    this favours a sparse data storage choice.
    """
    self._cells = set()

  def __call__(self):
    return self.cells

  def Around(self, origin):
    '''Same as AroundInclusive but does not include the given centre point.
    '''
    output = list(self.AroundInclusive(origin))

    """remove centre cell (the origin value):
    which is [0] or [0,0] or [0,0,0] etc."""
    del output[len(output) // 2]

    return tuple(output)

  def AroundInclusive(self, origin):
    '''Like AroundList but can take advantage of the fact that check
    [-1,0,1] is the same for all dimensions.
    '''
    if not origin: origin = (self.ORIGIN,) * self.dimensions

    dimensionValues = map(Check, origin)
    return tuple(itertoolsProduct(*dimensionValues))

  def AroundList(self, size=None, origin=None):
    '''Returns tuples of co-ordinates for a given range.
    Built from ideas learned on the making of Around().
    '''
    if not size: size = (self.SIZE,) * self.dimensions
    if not origin: origin = (self.ORIGIN,) * self.dimensions

    def LowHigh(size, origin):
      return range(origin, origin + size)

    # http://www.daniweb.com/software-development/python/threads/272931

    dimensionalRanges = map(LowHigh, *self.FixRange(size, origin))
    return tuple(itertoolsProduct(*dimensionalRanges))

  def CountAround(self, cell):
    '''Add up all the presant has_keys for all those Around()
    a given cell in the 'Current Array'.
    '''
    return sum(p in self.cells for p in self.Around(cell))

  def WillBeAlive(self, cell):
    '''Will a given cell be alive in the next generation?
    '''
    return self._currRule.IsAliveNextGeneration(self.GetCell(cell), self.CountAround(cell))

  def AffectableCells(self):
    '''All the live cells and all those around them within range of checking without duplicates.
    '''
    return set(c for cell in self.cells for c in self.AroundInclusive(cell))

  def Iterate(self):
    '''Do a single iteration.
    '''
    self._cells = set(cell for cell in self.AffectableCells() if self.WillBeAlive(cell))
    self._generation.Inc()

  def IterateMany(self, number=1):
    '''Do a single iteration by default or multiple if specified.
    '''
    number = ValidateToActualWholeNumber(number)
    for i in range(number):
      self.Iterate()

  def Random(self, size=None, origin=None):
    '''A minus size will just select in the other direction.
    Has to be limited so it doesn't try to assign a value to
    every coordinate in infinity.
    '''
    if size == None: size = (self.SIZE,) * self.dimensions
    if origin == None: origin = (self.ORIGIN,) * self.dimensions

    for cell in self.AroundList(*self.FixRange(size, origin)):
      self.SetCell(cell, RandomBoolean())

  def GetCell(self, cell):
    return cell in self.cells

  def SetCellSwap(self, cell):
    self.SetCell(cell, not self.GetCell(cell))

  def SetCell(self, cell, value=True):  
    if value:
      self.cells.add(cell)
    elif cell in self.cells:
      self.cells.remove(cell)

  def SetCellsAlive(self, *cells):
    list(map(self.SetCell, cells))

  def SetCells(self, *cells):
    '''Multiple SetCellSwap Calls in a single call.
    '''
    list(map(self.SetCellSwap, cells))

  def Glider(self):
    '''OXO
    OOX
    XXX
    '''
    self.SetCellsAlive((1,0), (2,1), (0,2), (1,2), (2,2))

  def GosperGliderGun(self):
    self.SetCellsAlive(
      (0,6), (0,7), (1,6), (1,7), #block
      (8,7), (8,8), (9,6), (9,8), (10,6), (10,7), #beehive
      (16,8), (16,9), (16,10), (17,8), (18,9), #glider
      (22,5), (22,6), (23,4), (23,6), (24,4), (24,5), #beehive
      (34,4), (34,5), (35,4), (35,5), #block
      (24,16), (24,17), (25,16), (25,18), (26,16), #glider
      (35,11), (35,12), (35,13), (36,11), (37,12), #gliders
    )

  def FixRange(self, size, origin):
    '''If a dimension is a minus size it it converted to positive
    and the origin is adjusted to compensate.
    This is done for all dimensions together.
    '''
    def Fix(sizeDim, originDim):
      if sizeDim < 0:
        sizeDim = -sizeDim
        originDim -= sizeDim
      return sizeDim, originDim

    """The zip should truncate the values to the smallest of
    the two in length (only applicable if they have different
    numbers of dimensions, which they should not)."""
    return tuple(zip(*map(Fix, size, origin)))

  def GetRange(self, size=None, origin=None):
    '''A minus size will just select in the other direction. Assumes 2D.
    '''
    if not size: size = (self.SIZE,) * self.dimensions
    if not origin: origin = (self.ORIGIN,) * self.dimensions

    size, origin = self.FixRange(size, origin)

    ranges = self.AroundList(size, origin)
    
    #depends upon number of dimensions and how AroundList is sorted
    dimensionWrapOn = 1
    
    linePlace = origin[dimensionWrapOn] + size[dimensionWrapOn]

    grid = []
    line = []
    for r in ranges:
      line.append(r in self.cells)
      #Is the end of a line?
      if r[dimensionWrapOn] == linePlace - 1:
        grid.append(line)
        line = []      
    return grid

  @property
  def population(self):
    '''As a side effect of storing co-ordinates as a sparse dataset,
    population does not have to be counted by exhaustive searching.
    '''
    return len(self.cells)

  @property
  def generation(self):
    return self._generation()

  @property
  def ruleStr(self):
    return self._currRule.string

  @ruleStr.setter
  def ruleStr(self, ruleStr):
    self._currRule.string = ruleStr

  @property
  def cells(self):
    return self._cells

  def __len__(self):
    return self.population

if __name__ == "__main__":
  def CellToChar(cellVal):
    '''input should be a bool.
    '''
    if cellVal:
      return CHAR_CELL_ALIVE
    else:
      return CHAR_CELL_DEAD

  def Display(grid):
    '''Because of the dimensional limitations of the display,
    only 2 dimensions can be handled in this manner
    (or one if given in the 2d format).
    '''
    return CHAR_SEP_LINE.join(
      [CHAR_SEP_CELL.join(
          [CellToChar(cell) for cell in line]
      ) for line in grid]
    )

  #None of these constants should be referred to by the class directly
  CHAR_CELL_ALIVE = 'X'
  CHAR_CELL_DEAD = '-'
  CHAR_SEP_CELL = ''
  CHAR_SEP_LINE = '\n'
  
  SIZE_NUM = 6
  ORIGIN_NUM = 0
  DIMENSIONS = 2

  GLIDER_PERIOD = 4

  print('Game Of Life - Testing')
  
  #ranging = (6, 6), (0, 0)
  ranging = (SIZE_NUM,) * DIMENSIONS, (ORIGIN_NUM,) * DIMENSIONS

  GOL = GameOfLife()

  GOL.Glider()
  #GOL.GosperGliderGun()

  for r in range(-1, GLIDER_PERIOD):
    '''Display every time including when r == -1 but only Iterate() from 0,
    so that the initial state is shown on screen.'''
    if not r < 0:
      GOL.Iterate()      
    print() #separate the displays
    print(Display(GOL.GetRange(*ranging)))

  print(GOL.population)
  print(GOL.ruleStr)
  print(GOL._currRule())
  print('%r' % GOL._currRule)

  print('\nAround Testing')
  a = GOL.Around((1,1,1))
  print(a[len(a) // 2])
  print((1,1,1) not in a)
  print((1,1,2) in a)
  
  print(a[len(a)-1] == (2,2,2))

  print('\nAroundList Testing')
  test = (2,2,2)
  a = GOL.AroundList(test, (1,1,1))
  print('a', a)
  print(a[len(a) - 1] == test)

  print('\nPopulation: ' + str(GOL.population))

  del(GOL)

  #keep the window open
  input('\nPress Enter to Close:')
