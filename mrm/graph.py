"""Graph Theory related helper functions"""

__all__ = ['bfs', 'connected_component', 'prim_mst']

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

def bfs(ngh, start_point, end_cond=lambda n: False):
    """Breadth-First Search
    Perform a breadth-first search, returning the dict mapping node id to iteration depth

    ngh -- dict mapping hashable node ids to list of neighbor node ids
    start_point -- node id of start point
    end_cond -- conditional function called for each point reached to end exploration early
    """
    component = set([start_point])
    curr_depth = 0
    depths = {start_point: curr_depth}
    while True:
        to_add = set(n for c in component for n in ngh[c] if n not in component)
        component |= to_add
        curr_depth += 1
        depths.update({a: curr_depth for a in to_add})
        if len(to_add) == 0:
            break
        if any(end_cond(a) for a in to_add):
            break
    return depths

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
