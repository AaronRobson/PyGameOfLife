from random import randrange

# RGB
_colour_min = 0x000000
_colour_max = 0xFFFFFF

assert _colour_min <= _colour_max


def hex_plain(number):
    '''Without 0x at the start.
    '''
    return '%X' % number


_colour_max_length = len(hex_plain(_colour_max))


def hex_plain_padded(number, padded_len):
    return hex_plain(number).zfill(padded_len)


def hex_colour_padded(colour_number, prefix=''):
    return str(prefix) + hex_plain_padded(colour_number, _colour_max_length)


def standard_hex_colour_padded(colour_number):
    return hex_colour_padded(colour_number, prefix='0x')


def tk_hex_colour_padded(colour_number):
    return hex_colour_padded(colour_number, prefix='#')


def colour_number_is_valid(colour_number):
    return _colour_min <= colour_number <= _colour_max


def random_colour():
    return randrange(_colour_min, _colour_max + 1)
