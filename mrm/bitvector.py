"""Module for a bitvector object with easily manipulated bits"""

__all__ = ['Bitvector']

from functools import total_ordering
from math import ceil, log2

@total_ordering
class Bitvector:
    """Bitvectors provide convenient access and manipulation of individual binary bits"""

    def __init__(self, *, max_bit: None|int=None, iv: int=0):
        """Creates a new Bitvector with initial value iv and with largest bit at least max_bit.
        If max_bit is None or not specified, it will be set to the closest multiple of 8
        capable of holding the iv.  If it is specified, it will also be set to the next highest
        multiple of 8 bits.
        """

        if iv < 0:
            raise ValueError(f'{iv=} must be >= 0')

        if iv == 0:
            need_bits = 1
        else:
            need_bits = ceil(log2(iv))

        if max_bit is None:
            max_bit = need_bits

        if max_bit < need_bits:
            raise ValueError(f'{iv=} needs {ceil(log2(iv))} bits, which is less than {max_bit=}')

        self.max_bit = ceil((max_bit + 1) / 8) * 8 - 1
        self.data = bytearray((self.max_bit + 1) // 8)
        for i, b in enumerate(reversed(bin(iv)[2:])):
            self[i] = b == '1'

    def __getitem__(self, bit: int) -> bool:
        """Returns the current state of the specified bit index"""
        if bit < 0 or bit > self.max_bit:
            raise IndexError(f'bit index out of range 0 to {self.max_bit}')
        return self.data[bit // 8] >> (bit % 8) & 0x01 == 1

    def __setitem__(self, bit: int, val: bool):
        """Sets the state of the specified bit index to val"""
        if bit < 0 or bit > self.max_bit:
            raise IndexError(f'bit index out of range 0 to {self.max_bit}')
        if val:
            self.data[bit // 8] |= 1 << (bit % 8)
        else:
            self.data[bit // 8] &= ~(1 << (bit % 8))

    def as_int(self) -> int:
        """Returns the set bits as an unsigned int"""
        return int.from_bytes(self.data, byteorder='little')

    def bits(self) -> list[int]:
        """Returns a list of currently set bit numbers"""
        return [x for x in range(self.max_bit + 1) if self[x]]

    def without(self, bit: int) -> 'Bitvector':
        """Chainable function to clear a specific bit
        (returns the Bitvector being operated on)
        """
        self[bit] = False
        return self

    def with_(self, bit: int) -> 'Bitvector':
        """Chainable item to set a specific bit
        (returns the Bitvector being operated on)
        """
        self[bit] = True
        return self

    def copy_with(self, bit: int) -> 'Bitvector':
        """Chainable item to set a specific bit
        (returns a new Bitvector being operated on)
        """
        bv = Bitvector(max_bit=self.max_bit, iv=self.as_int())
        bv[bit] = True
        return bv

    def __repr__(self):
        return 'bitvect<' + bin(self.as_int()) + '>'

    def __lt__(self, other) -> bool:
        """Returns a < b for two Bitvectors,
        which are compared based on their as_int() values.
        """
        if not isinstance(other, Bitvector):
            return NotImplemented
        return self.as_int() < other.as_int()

    def __eq__(self, other) -> bool:
        """Returns a == b for two Bitvectors,
        which are compared based on their as_int() values.
        """
        if not isinstance(other, Bitvector):
            return NotImplemented
        return self.as_int() == other.as_int()

    def __hash__(self) -> int:
        """Returns hash of Bitvector, which is its as_int() value."""
        return self.as_int()

    @staticmethod
    def from_bits(bit_list: list[int], max_bit: None|int=None) -> 'Bitvector':
        """Creates a Bitvector with all bits in bit_list preset.
        max_bit may be specified or it will be calculated automatically.
        """
        v = Bitvector(max_bit=max_bit)
        for b in bit_list:
            v[b] = True
        return v
