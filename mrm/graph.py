"""Graph Theory related helper functions"""

__all__ = ['bfs_dist', 'bfs_min_paths', 'connected_component', 'prim_mst']

from collections import defaultdict, deque

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

def bfs_dist(ngh, start_point):
    """Breadth-First Search
    Perform a breadth-first search, returning the dict mapping node id to iteration depth

    ngh -- dict mapping hashable node ids to list of neighbor node ids
    start_point -- node id of start point
    """
    weights = {start_point: 0}
    explore_from = deque([start_point])
    explored = set()
    while explore_from:
        src = explore_from.popleft()
        if src in explored:
            continue
        explored.add(src)
        dst = [n for n in ngh[src] if n not in explored and n not in explore_from]
        for d in dst:
            weights[d] = weights[src] + 1
            explore_from.append(d)
    return weights

def bfs_min_paths(ngh, start_point):
    """Breadth-First Search (all min paths)
    Perform a breadth-first search, returning the dict mapping node id to all min paths

    ngh -- dict mapping hashable node ids to list of neighbor node ids
    start_point -- node id of start point
    """
    paths = defaultdict(list)
    paths[start_point] = [[start_point]]
    explore_from = deque([start_point])
    explored = set()
    while explore_from:
        src = explore_from.popleft()
        if src in explored:
            continue
        explored.add(src)
        dst = [n for n in ngh[src] if n not in explored]
        for d in dst:
            paths[d] += [p + [d] for p in paths[src]]
            if d not in explore_from:
                explore_from.append(d)
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
