"""Module for parsing helper functions"""

__all__ = ['ensure_equal_length']

def ensure_equal_length(lines, pad_char=' '):
    """Pads any short lines to the length of the longest line with pad_char"""
    longest = max(len(l) for l in lines)
    return [f'{l:{pad_char}<{longest}s}' for l in lines]
