#!/usr/bin/python

from string import digits

_STRING_RULE_SEPARATOR = '/'

#'3/23'
_CONWAY_STANDARD_STRING_RULE = _STRING_RULE_SEPARATOR.join(['3', '23'])

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
    return _STRING_RULE_SEPARATOR.join([
          #inner one makes a generator object rather than a list directly, speeds up 
          ''.join((str(int(num)) for num in subList))
        for subList in rule[:2]
    ])

  def _StringToRule(self, stringRule=None):
    '''Returns the rule data structure of an inputted string notation.
    If no string is specified the John Conway standard rule string is used
    Exactly opposite to StringToRule when using valid notations.
    '''
    if stringRule is None: stringRule = _CONWAY_STANDARD_STRING_RULE

    splitRules = stringRule.split(_STRING_RULE_SEPARATOR)

    #All after the second '/' if present is ignored
    output = [()]*2
    count = min(len(output), len(splitRules))
    for s in range(count):
      #if char not in string .digits ignore it as bad value and move on
      output[s] = self._StringToDigitTuple(splitRules[s])
    return tuple(output)

if __name__ == "__main__":
  print('"Rule" support unit.')

  #keep the window open
  input('\nPress Enter to Close:')