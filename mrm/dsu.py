"""Disjoint Set Union"""

__all__ = ['DisjointSetUnion']

class DisjointSetUnion:
    """Disjoint Set Union
    Stores a union of disjoint sets and provides optimized set union and membership find functions
    """
    def __init__(self):
        self._parent = {}
        self._size = {}

    def add_set(self, iterable):
        """Adds a new set from an iterable list of items
        iterable -- iterable to add as a set
        """
        if not iterable:
            raise ValueError('iterable must contain at least one item')
        it = iter(iterable)
        if any(m in self._parent for m in it):
            raise ValueError('Items must not already be in a set')
        it = iter(iterable)
        p = next(it)
        self._parent[p] = p
        cnt = 1
        for m in it:
            self._parent[m] = p
            cnt += 1
        self._size[p] = cnt

    def add_nodes(self, iterable):
        """Adds new sets each containing one item from the iterable
        iterable -- iterable to add as individual sets
        """
        if not iterable:
            raise ValueError('iterable must contain at least one item')
        it = iter(iterable)
        if any(m in self._parent for m in it):
            raise ValueError('Items must not already be in a set')
        it = iter(iterable)
        for p in it:
            self._parent[p] = p
            self._size[p] = 1

    def find(self, m):
        """Finds the representative set parent for a given member
        m -- set member to find
        """
        if m not in self._parent:
            raise ValueError(f'{m} not present in any set')
        if m == self._parent[m]:
            return m
        self._parent[m] = self.find(self._parent[m])
        return self._parent[m]

    def union(self, m1, m2):
        """Joins the set or sets containing the given pair of members
        m1 -- first member
        m2 -- second member
        Returns True if members were not already in same set, else False
        """
        if m1 not in self._parent:
            raise ValueError(f'{m1} not present in any set')
        if m2 not in self._parent:
            raise ValueError(f'{m2} not present in any set')
        m1 = self.find(m1)
        m2 = self.find(m2)
        if m1 == m2:
            return False
        s1 = self._size[m1]
        s2 = self._size[m2]
        if s1 < s2:
            m1, m2 = m2, m1
        self._parent[m2] = m1
        self._size[m1] += self._size[m2]
        del self._size[m2]
        return True

    def sets(self):
        """Compresses all paths and returns the resultant sets
        as a dict mapping representative to all set members
        """
        for p in self._parent:
            self.find(p)
        return {pk: set(sk for sk, sv in self._parent.items() if sv==pk) for pk in set(self._parent.values())}

    def __contains__(self, m):
        """Member exists in any set"""
        return m in self._parent

    def __len__(self):
        """Total number of items in all sets"""
        return len(self._parent)
