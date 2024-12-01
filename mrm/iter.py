"""Module for iterator helper functions"""

__all__ = ['batched', 'sliding_window']

from collections import deque
from itertools import islice

def batched(iterable, batch_size = 2):
    """Splits iterable into batch_size pieces
    Provided by itertools directly in Python 3.12+
    """
    it = iter(iterable)
    while batch := tuple(islice(it, batch_size)):
        yield batch

def sliding_window(iterable, win_size = 2):
    """Moves through iterable in win_size length windows"""
    it = iter(iterable)
    d = deque()
    for _ in range(win_size):
        d.append(next(it, None))
    yield tuple(d)
    for x in it:
        d.popleft()
        d.append(x)
        yield tuple(d)
