#!/usr/bin/python

from string import digits

_STRING_RULE_SEPARATOR = '/'

# '3/23'
_CONWAY_STANDARD_STRING_RULE = _STRING_RULE_SEPARATOR.join(['3', '23'])

def _StringToDigitTuple(digitString):
    '''Sorts and removes duplicates.
    Returns the canonical representation.
    '''
    return tuple(sorted(set(int(char) for char in digitString if str(char) in digits)))

def _RuleToString(rule):
    '''Returns the string notation of an inputted rule data structure,
    Exactly opposite to StringToRule when using valid notations.
    '''

    # outer one uses a direct list as join takes longer to deal with generator objects
    return _STRING_RULE_SEPARATOR.join([
        # inner one makes a generator object rather than a list directly, speeds up 
        ''.join((str(int(num)) for num in subList))
      for subList in rule[:2]
    ])

def _StringToRule(stringRule=None):
    '''Returns the rule data structure of an inputted string notation.
    If no string is specified the John Conway standard rule string is used
    Exactly opposite to StringToRule when using valid notations.
    '''
    if stringRule is None: stringRule = _CONWAY_STANDARD_STRING_RULE

    splitRules = stringRule.split(_STRING_RULE_SEPARATOR)

    # All after the second '/' if present is ignored
    output = [()]*2
    count = min(len(output), len(splitRules))
    for s in range(count):
        # if char not in string .digits ignore it as bad value and move on
        output[s] = _StringToDigitTuple(splitRules[s])
    return tuple(output)

class Rule():
    def __init__(self, ruleStr=None):
        self._born, self._survives = _StringToRule(ruleStr)

    def __str__(self):
        return _RuleToString((self._born, self.survives,))

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    def __call__(self):
        return str(self)

    @property
    def born(self):
        return self._born

      @property
      def survives(self):
        return self._survives

    def IsAliveNextGeneration(self, aliveNow, liveCellsAround):
        if aliveNow:
            allowed = self.survives
        else:
            allowed = self.born

        return liveCellsAround in allowed

if __name__ == "__main__":
    print('"Rule" support unit.')
    print()
    rule = Rule()
    print(repr(rule))
    print(rule)
    print('born:', rule.born)
    print('survives:', rule.survives)

    #keep the window open
    input('\nPress Enter to Close:')
