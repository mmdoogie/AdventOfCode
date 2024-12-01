"""Module for small helper functions without a home"""

__all__ = ['big_pi', 'md5sum', 'product']

from functools import reduce
from hashlib import md5
from operator import mul

def md5sum(s):
    """Provides the hex-encoded MD5 hash of a string"""
    return md5(s.encode('utf-8')).hexdigest()

def product(x):
    """Multiplies all elements of an iterable together"""
    return reduce(mul, x)

big_pi = product
