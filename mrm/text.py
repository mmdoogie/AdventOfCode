"""Module for text manipulation helpers"""

__all__ = ['let2num', 'num2let']

def let2num(letter):
    """Converts letter to its number position in the alphabet
    a/A -> 0, z/Z -> 25
    """
    return ord(letter.lower()) - ord('a')

def num2let(num):
    """Converts num position in the alphabet to its letter
    0 -> a, 25 -> z
    """
    return chr(num + ord('a'))
