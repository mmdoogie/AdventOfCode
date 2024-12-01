"""Module for dealing with 2D points and directions using complex numbers"""

ZERO = 0j
UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1

def left_turn(heading):
    """Returns new heading after making a left turn from passed heading"""
    return heading * -1j

def right_turn(heading):
    """Returns new heading after making a right turn from passed heading"""
    return heading * 1j

def u_turn(heading):
    """Returns new heading after making a U turn from passed heading"""
    return heading * -1

def go_dist(from_pt, heading, dist):
    """Returns point reached after traveling dist units from from_pt in direction of heading"""
    return from_pt + dist * heading

def as_xy(pt, t=float):
    """Converts complex point to cartesian components. t can be used to specify int/float."""
    return t(pt.real), t(pt.imag)

def from_xy(x, y):
    """Makes a complex point from cartesian components"""
    return x + 1j * y

def adj_ortho(pt, constrain_pos = None):
    """Returns list of orthogonally adjacent positions (left, up, right, down)
    subject to being present in constrain_pos (use None to always return all four).
    """
    adj = [pt + o for o in [-1, -1j, 1, 1j]]
    if constrain_pos is None:
        return adj
    return [a for a in adj if a in constrain_pos]

def adj_diag(pt, constrain_pos = None):
    """Returns list of orthogonally and diagonally adjacent positions (up-left, left, down-left,
    up, down, up-right, right, down-right) subject to being present in constrain_pos (use None
    to always return all four).
    """
    adj = [pt + y + x for y in [-1j, 0, 1j] for x in [-1, 0, 1] if any([x, y])]
    if constrain_pos is None:
        return adj
    return [a for a in adj if a in constrain_pos]

def m_dist(pt1, pt2 = ZERO):
    """Return Manhattan / grid distance between two points, or origin if pt2 not specified"""
    return abs(pt2.real - pt1.real) + abs(pt2.imag - pt1.imag)

def dist(pt1, pt2 = ZERO):
    """Return vector distance between two points, or origin if pt2 not specified"""
    return abs(pt2 - pt1)

def grid_as_dict(grid, valid = lambda x: True):
    """Convert a grid of text into a dictionary of complex points mapping to corresponding characters.
    Points are only included subject to the valid function (defaults to accepting all points).
    """
    res = {}
    for y, g in enumerate(grid):
        for x, c in enumerate(g):
            if valid(c):
                res[from_xy(x, y)] = c
    return res
