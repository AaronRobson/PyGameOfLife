#!/usr/bin/python

from random import randrange

# RGB
_COLOUR_MIN = 0x000000
_COLOUR_MAX = 0xFFFFFF

assert _COLOUR_MIN <= _COLOUR_MAX

def HexPlain(number):
    '''Without 0x at the start.
    '''
    return '%X' % number

_COLOUR_MAX_LENGTH = len(HexPlain(_COLOUR_MAX))

def HexPlainPadded(number, paddedLen):
    return HexPlain(number).zfill(paddedLen)

def HexColourPadded(colourNumber, prefix=''):
    return str(prefix) + HexPlainPadded(colourNumber, _COLOUR_MAX_LENGTH)

def StandardHexColourPadded(colourNumber):
    return HexColourPadded(colourNumber, prefix='0x')

def TKHexColourPadded(colourNumber):
    return HexColourPadded(colourNumber, prefix='#')

def ColourNumberIsValid(colourNumber):
    return _COLOUR_MIN <= colourNumber <= _COLOUR_MAX

def RandomColour():
    return randrange(_COLOUR_MIN, _COLOUR_MAX + 1)

if __name__ == "__main__":
    print('"colourutils" support unit.')
    input('\nPress Enter to Close:')
