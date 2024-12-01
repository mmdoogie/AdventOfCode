"""Module for linked list"""

__all__ = ['llist']

class _lle:
    """Linked List Element"""

    def __init__(self, val, el_prev = None, el_next = None):
        """Create new LLE with value val and potential initial prev/next elements"""
        self.val = val
        self._prev = el_prev
        self._next = el_next

    def right(self):
        """Return element to the right of this element"""
        return self._next

    def left(self):
        """Return element to the left of this element"""
        return self._prev

    def far_right(self, amt):
        """Return element amt items to the right of this element"""
        el = self
        for _ in range(amt):
            el = el.right()
        return el

    def far_left(self, amt):
        """Return element amt items to the left of this element"""
        el = self
        for _ in range(amt):
            el = el.left()
        return el

class llist:
    """Linked List"""

    def __init__(self, items, circular = False):
        """Create a linked list with initial items, optionally circular."""
        prev = None
        self._circular = False
        self._nodecount = 0
        for i in items:
            el = _lle(i, prev)
            if prev is None:
                self._head = el
            else:
                el._prev._next = el
            prev = el
            self._nodecount += 1
        if circular:
            self._circular = True
            self._head._prev = el
            el._next = self._head

    def head(self):
        """Return the head element.
        This may change if items are inserted to the left of this element."""
        return self._head

    def __iter__(self):
        """Iterator for one pass through the entire linked list"""
        return self._itgen()

    def _itgen(self):
        el = self._head
        yield el
        while True:
            el = el.right()
            if el is None or el is self._head:
                break
            yield el

    def insert_right_of(self, node, val):
        """Insert a new element to the right of node with value val"""
        new_el = _lle(val, node)
        new_el._next = node._next
        if node._next:
            node._next._prev = new_el
        node._next = new_el
        self._nodecount += 1
        return new_el

    def insert_left_of(self, node, val):
        """Insert a new element to the left of node with value val"""
        new_el = _lle(val, node._prev, node)
        if node._prev:
            node._prev._next = new_el
        node._prev = new_el
        self._nodecount += 1
        if node == self._head:
            self._head = new_el
        return new_el

    def drop(self, node):
        """Drop element node from the list and relink adjacents"""
        if node._prev:
            node._prev._next = node._next
        if node._next:
            node._next._prev = node._prev
        if node is self._head:
            self._head = node._next
        self._nodecount -= 1

    def __len__(self):
        """Return number of elements currently in the list"""
        return self._nodecount

    def find(self, val):
        """Search the linked list from the head returing the first node with value val"""
        pass_two = False
        for x in self:
            if x is self._head and pass_two:
                return None
            if x is self._head:
                pass_two = True
            if x.val == val:
                return x
        return None
