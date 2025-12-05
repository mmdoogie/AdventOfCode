"""Module for small helper functions without a home"""

__all__ = ['big_pi', 'Funkydict', 'md5sum', 'product', 'repeatedly_apply', 'merge_ranges']

from collections import UserDict
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

class Funkydict(UserDict):
    """Dict-like object that immediately applies a reducing function when items are set

    initial_data: data to load prior to operation
    set_fun: function taking current and new value and returning reduced/accumulated value to store
    defaultfactory: function to create the base value for new keys
    """

    def __init__(self, initialdata = None, set_fun = lambda curr, new: new, default_factory = int):
        if initialdata:
            super().__init__(initialdata)
        else:
            super().__init__()
        self.set_fun = set_fun
        self.default_factory = default_factory

    def __setitem__(self, key, val):
        if key in self:
            curr = self[key]
        else:
            curr = self.default_factory()
        self.data[key] = self.set_fun(curr, val)

def repeatedly_apply(fn, iv, times, *args, **kwargs):
    """Repeatedly apply a function to it's previous value"""
    val = iv
    for _ in range(times):
        val = fn(val, *args, **kwargs)
    return val

def merge_ranges(ranges):
    """Merge a set or list of ranges so that there are no entries covered by more than one range"""

    ranges = sorted(ranges, key=lambda x: x.start)
    while True:
        del_ranges = set()
        add_ranges = set()
        for r1 in ranges:
            for r2 in ranges:
                if r1 == r2:
                    continue
                if r2.start < r1.start:
                    continue
                if r2.start > r1.stop:
                    break
                if r2.stop <= r1.stop:
                    del_ranges.add(r2)
                    break
                if r2.stop > r1.stop:
                    del_ranges.add(r1)
                    del_ranges.add(r2)
                    add_ranges.add(range(r1.start, r2.stop))
                    break
            if add_ranges or del_ranges:
                ranges = sorted(set(ranges).difference(del_ranges).union(add_ranges), key=lambda x: x.start)
                break
        if not add_ranges and not del_ranges:
            break

    return ranges
