"""Graph Theory related helper functions"""

__all__ = ['bfs_dist', 'bfs_min_paths', 'connected_component', 'prim_mst']

from collections import defaultdict, deque
from .prioset import Prioset

def connected_component(ngh, start_point):
    """Connected Component
    Returns the set of nodes that form a connected component using the provided neighbors

    ngh -- dict mapping hashable node ids to list of neighbor node ids
    start_point -- one node id in the desired component
    """
    component = set([start_point])
    while True:
        to_add = set(n for c in component for n in ngh[c] if n not in component)
        component |= to_add
        if len(to_add) == 0:
            break
    return component

def bfs_dist(ngh, start_point, max_dist=0):
    """Breadth-First Search
    Perform a breadth-first search, returning the Prioset of nodes reached at each depth

    ngh -- dict mapping hashable node ids to list of neighbor node ids
    start_point -- node id of start point
    max_dist -- optional: maximum depth to explore, 0 (default) is unlimited
    """
    weights = Prioset()
    weights.add(start_point, 0)
    explore_from = Prioset()
    explore_from.add(start_point, 0)
    while explore_from:
        src, src_wt = explore_from.pop()
        dst_wt = src_wt + 1
        for d in ngh[src]:
            weights.add(d, dst_wt)
            if not max_dist or dst_wt < max_dist:
                explore_from.add(d, dst_wt)
    return weights

def bfs_min_paths(ngh, start_point):
    """Breadth-First Search (all min paths)
    Perform a breadth-first search, returning the dict mapping node id to all min paths

    ngh -- dict mapping hashable node ids to list of neighbor node ids
    start_point -- node id of start point
    """
    paths = defaultdict(list)
    paths[start_point] = [[start_point]]
    explore_from = Prioset()
    explore_from.add(start_point, 0)
    explored = set()
    while explore_from:
        src, src_wt = explore_from.pop()
        if src in explored:
            continue
        explored.add(src)
        dst_wt = src_wt + 1
        for d in ngh[src]:
            paths[d] += [p + [d] for p in paths[src]]
            explore_from.add(d, dst_wt)
    return paths

def prim_mst(ngh, wts, start_point=None):
    """Prim's Algorithm for Minimum Spanning Tree
    Computes the minimum spanning tree for a graph using the provided neighbors and weights.
    Returns the nodes and edges defining the MST of the connected component reachable from start_point.

    ngh -- dict mapping hashable node ids to list of neighbor node ids
    wts -- dict mapping (src, dest) node ids to weight of edge
    start_point -- will be used as initial point if provided, otherwise one is randomly chosen
    """
    in_set = set()
    out_set = set(ngh)
    edges = []
    if start_point is None:
        start_point = out_set.pop()
    else:
        if len(ngh.get(start_point, [])) != 0:
            out_set.remove(start_point)
    in_set.add(start_point)
    while out_set:
        rem_dists = [(wts[pair := (a, b)], pair) for a in in_set for b in ngh[a] if b not in in_set]
        if len(rem_dists) == 0:
            return in_set, edges
        choose = min(rem_dists)[1]
        edges += [choose]
        in_set.add(choose[1])
        out_set.remove(choose[1])
    return in_set, edges
