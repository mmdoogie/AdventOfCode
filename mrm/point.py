"""Module for arbitrary-dimension points using tuples"""

__all__ = ['ZERO_2D', 'ZERO_3D', 'adj_ortho', 'adj_diag', 'm_dist', 'dist',
           'point_add', 'point_sub', 'point_neg', 'grid_as_dict', 'polygon_area',
           'polygon_border_dist', 'polygon_interior_squares', 'polygon_grid_squares']

from itertools import pairwise, product

ZERO_2D = (0, 0)
ZERO_3D = (0, 0, 0)

def adj_ortho(pt, constrain_pos = None):
    """Returns list of positions which are orthogonally adjacent in all dimensions
    subject to being present in constrain_pos (use None to always return the full list).
    """
    dims = len(pt)
    adj = [(*pt[:d], pt[d] + o, *pt[d + 1:]) for d in range(dims) for o in [-1, 1]]
    if constrain_pos is None:
        return adj
    return [a for a in adj if a in constrain_pos]

def adj_diag(pt, constrain_pos = None):
    """Returns list of positions which are orthogonally or diagonally adjacent in all dimensions
    subject to being present in constrain_pos (use None to always return the full list).
    """
    dims = len(pt)
    adj = [tuple(pt[i] + o[i] for i in range(dims)) for o in product([-1, 0, 1], repeat = dims) if any(o)]
    if constrain_pos is None:
        return adj
    return [a for a in adj if a in constrain_pos]

def m_dist(pt1, pt2):
    """Return Manhattan / grid distance between two points"""
    if len(pt1) != len(pt2):
        raise ValueError('Point lengths must match to compute distance')
    return sum(abs(a - b) for a, b in zip(pt1, pt2))

def dist(pt1, pt2):
    """Return vector distance between two points"""
    if len(pt1) != len(pt2):
        raise ValueError('Point lengths must match to compute distance')
    return sum((a - b) ** 2 for a, b in zip(pt1, pt2)) ** 0.5

def point_add(pt1, pt2):
    """Return new point which is the sum pt1 + pt2 of all dimension components"""
    if len(pt1) != len(pt2):
        raise ValueError('Point lengths must match to compute sum')
    return tuple(a + b for a, b in zip(pt1, pt2))

def point_sub(pt1, pt2):
    """Return new point which is the difference pt1 - pt2 of all dimension components"""
    if len(pt1) != len(pt2):
        raise ValueError('Point lengths must match to compute difference')
    return tuple(a - b for a, b in zip(pt1, pt2))

def point_neg(pt):
    """Return new point which is the negation of all dimension components"""
    return tuple(-p for p in pt)

def grid_as_dict(grid, valid = lambda x: True):
    """Convert a grid of text into a dictionary of 2D points mapping to corresponding characters.
    Points are only included subject to the valid function (defaults to accepting all points).
    """
    res = {}
    for y, g in enumerate(grid):
        for x, c in enumerate(g):
            if valid(c):
                res[(x, y)] = c
    return res

def polygon_area(pts):
    """Calculate the contained area inside a polygon defined by the list of points given
    using the Shoelace formula.
    """
    if len(pts[0]) != 2:
        raise ValueError('Polygon functions are only defined for 2D points')
    x = [p[0] for p in pts]
    y = [p[1] for p in pts]
    if x[0] != x[-1] or y[0] != y[-1]:
        x += [x[0]]
        y += [y[0]]
    cross1 = sum(x1 * y2 for x1, y2 in zip(x, y[1:]))
    cross2 = sum(x2 * y1 for x2, y1 in zip(x[1:], y))
    if cross2 < cross1:
        return (cross1 - cross2) / 2
    return (cross2 - cross1) / 2

def polygon_border_dist(pts, dist_fn = m_dist):
    """Calculate the perimeter distance of a polygon defined by the list of points given
    the dist_fn could be m_dist (default) for points on a grid or dist for the precise value.
    """
    pts = list(pts)
    if pts[0] != pts[-1]:
        pts += [pts[0]]
    return sum(dist_fn(a, b) for a, b in pairwise(pts))

def polygon_interior_squares(pts):
    """Compute the number of integer grid points contained inside a polygon with integer pts
    using Pick's Theorem.
    """
    area = polygon_area(pts)
    border = polygon_border_dist(pts)
    return area - border / 2 + 1

def polygon_grid_squares(pts):
    """Compute the number of integer grid squares covered by the border and interior of
    a polygon with integer pts.
    """
    return polygon_interior_squares(pts) + polygon_border_dist(pts)
