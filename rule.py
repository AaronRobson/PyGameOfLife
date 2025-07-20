from string import digits

_string_rule_separator = '/'

# '3/23'
_conway_standard_string_rule = _string_rule_separator.join(['3', '23'])


def _string_to_digit_tuple(digit_string):
    '''Sorts and removes duplicates.
    Returns the canonical representation.
    '''
    return tuple(sorted(set(
        int(char)
        for char in digit_string
        if str(char) in digits)))


def _rule_to_string(rule):
    '''Returns the string notation of an inputted rule data structure,
    Exactly opposite to StringToRule when using valid notations.
    '''
    return _string_rule_separator.join([
        ''.join((str(int(num)) for num in sub_list))
        for sub_list in rule[:2]
    ])


def _string_to_rule(string_rule=None):
    '''Returns the rule data structure of an inputted string notation.
    If no string is specified the John Conway standard rule string is used
    Exactly opposite to StringToRule when using valid notations.
    '''
    if string_rule is None:
        string_rule = _conway_standard_string_rule

    split_rules = string_rule.split(_string_rule_separator)

    # All after the second '/' if present is ignored
    output = [()]*2
    count = min(len(output), len(split_rules))
    for s in range(count):
        # if char not in string .digits ignore it as bad value and move on
        output[s] = _string_to_digit_tuple(split_rules[s])
    return tuple(output)


class Rule():
    def __init__(self, rule_str=None):
        self._born, self._survives = _string_to_rule(rule_str)

    def __str__(self):
        return _rule_to_string((self._born, self.survives,))

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    @property
    def born(self):
        return self._born

    @property
    def survives(self):
        return self._survives

    def is_alive_next_generation(self, alive_now, live_cells_around):
        if alive_now:
            allowed = self.survives
        else:
            allowed = self.born

        return live_cells_around in allowed


if __name__ == '__main__':
    print('Standard Conway rules (Born/Survives): %s' % Rule())