"""Module for parsing helper functions"""

__all__ = ['all_nums', 'ensure_equal_length', 'int_if_possible']

import re

def ensure_equal_length(lines, pad_char=' '):
    """Pads any short lines to the length of the longest line with pad_char"""
    longest = max(len(l) for l in lines)
    return [f'{l:{pad_char}<{longest}s}' for l in lines]

_INTS_RE = re.compile(r'(-?[0-9]+)')
_FLOATS_RE = re.compile(r'(-?[0-9]+\.?[0-9]*)')

def all_nums(line, int_or_float=int):
    """Returns a generator on all numbers embedded in a line of text.
    int_or_float: function used to parse extracted text;
    the regex used for extraction is int-focused only if this is 'int'.
    """
    regex = _INTS_RE
    if int_or_float is not int:
        regex = _FLOATS_RE
    return (int_or_float(match[0]) for match in regex.finditer(line))

def int_if_possible(s):
    """Returns int conversion of an object if possible,
    otherwise the original object is returned
    """
    v = s

    try:
        v = int(s)
    except ValueError:
        pass

    return v
