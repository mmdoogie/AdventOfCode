"""Contains tools for dealing with Chinese Remainder Theorem style problems"""

__all__ = ['all_coprime', 'coprime', 'crt']

from functools import reduce
from itertools import combinations
from operator import mul
from math import gcd

def coprime(a: int, b: int) -> bool:
    """Returns true if the pair of integers given are coprime"""
    return gcd(a, b) == 1

def all_coprime(vals: list[int]) -> bool:
    """Returns true if all pairs of integers given are coprime"""
    return all(coprime(a, b) for a, b in combinations(vals, 2))

def crt(vals: list[int], mods: list[int]) -> int:
    """Chinese Remainder Theorem
    Computes n such that [n % m for m in mods] == vals
    All pairs of modulos must be relatively coprime.
    """
    if not all_coprime(mods):
        for a, b in combinations(mods, 2):
            if not coprime(a, b):
                raise ValueError(f'{a} and {b} are not coprime')

    for v, m in zip(vals, mods):
        if v >= m:
            raise ValueError(f'remainder {v} is invalid for mod {m}')

    mod_prod = reduce(mul, mods)
    isolates = [mod_prod // m for m in mods]

    factors = []
    for iso, mod, val in zip(isolates, mods, vals):
        if iso % mod == val:
            factors += [1]
            continue
        f = 2
        while (iso * f) % mod != val:
            f += 1
        factors += [f]

    test_val = sum(iso * fact for iso, fact in zip(isolates, factors))
    while test_val > mod_prod:
        test_val -= mod_prod

    return test_val
