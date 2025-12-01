"""Priority Set"""

__all__ = ['Prioset']

import heapq

class Prioset:
    """Priority Set
    Provides a priority queue implemented with sets for faster insertion & membership checking
    """
    def __init__(self, max_heap=False):
        """Create a new empty Priority Set

        max_heap -- if True, uses a max heap, where pop instead returns an item from the maximal priority level
        """
        self._sets = {}
        self._prios = []
        self._max_heap = max_heap

    def add(self, item, prio):
        """Add a new item with associated priority level

        item -- item to add
        prio -- priority of item to add
        """
        if self._max_heap:
            prio = -prio
        if prio in self._sets:
            self._sets[prio].add(item)
            return
        self._sets[prio] = {item}
        heapq.heappush(self._prios, prio)

    def pop(self):
        """Retrieve a random item from the minimum priority level

        Returns item and its associated priority level
        """
        if not self._prios:
            raise IndexError('No values to pop')
        prio = self._prios[0]
        item = self._sets[prio].pop()
        if not self._sets[prio]:
            heapq.heappop(self._prios)
            del self._sets[prio]
        if self._max_heap:
            prio = -prio
        return item, prio

    def prios(self):
        """Get the list of priority levels present"""
        if self._max_heap:
            return sorted((-s for s in self._prios), reverse=True)
        return sorted(self._prios)

    def __bool__(self):
        """Returns true if any priority levels are present"""
        return bool(self._prios)

    def __len__(self):
        """Returns total count of all contained items"""
        return sum(len(s) for s in self._sets.values())

    def __contains__(self, key):
        """Checks for given item in all priority levels"""
        for s in self._sets.values():
            if key in s:
                return True
        return False

    def __getitem__(self, key):
        """Returns the set of items for a given priority level"""
        if self._max_heap:
            key = -key
        if key in self._sets:
            return self._sets[key]
        raise IndexError(f'Priority level {key} not present')

    def __iter__(self):
        return iter(self.prios())
