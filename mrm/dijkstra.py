"""Module for Dijkstra's Algorithm pathfinding"""

__all__ = ['dijkstra', 'Dictlike']

from collections import defaultdict

def dijkstra(neighbors_dict, weights_dict = defaultdict(lambda: 1), start_point = None,
             end_point = None, keep_paths = True, dist_est = lambda x: 0, danger_ignore_visited = False):
    """Performs a Dijkstra's Algorithm pathfinding using the neighbors and weights provided.
    Starts from start_point and ends either when all paths are exhausted (end_point=None),
    when the point end_point has been reached (end_point is a node), or when all end points are reached
    (end_point is a list/set).
    If keep_paths is False, only the final weights are returned.
    Providing an admissible distance estimator for dist_est converts this to A*.
    """
    visited = set()
    curr_point = start_point

    weights = {curr_point: 0}
    explore = defaultdict(set)
    if keep_paths:
        paths = {curr_point: [curr_point]}

    if isinstance(end_point, list):
        found_ends = {e: False for e in end_point}
    else:
        found_ends = {end_point: False}

    while True:
        if end_point is not None:
            if curr_point in found_ends:
                found_ends[curr_point] = True
            if curr_point == end_point:
                break
            if all(found_ends.values()):
                break
        if not danger_ignore_visited:
            visited.add(curr_point)
        if keep_paths:
            curr_path = paths[curr_point]
        if curr_point in neighbors_dict:
            for n in neighbors_dict[curr_point]:
                curr_weight = weights[curr_point] + weights_dict[(curr_point, n)]
                if n not in weights or curr_weight < weights[n]:
                    weights[n] = curr_weight
                    if keep_paths:
                        paths[n] = curr_path + [n]
                if n not in visited:
                    explore[curr_weight + dist_est(n)].add(n)

        buckets = sorted(explore.keys())
        while curr_point in visited or danger_ignore_visited:
            found_point = False
            for b in buckets:
                if len(explore[b]) != 0:
                    curr_point = explore[b].pop()
                    found_point = True
                    break
                del explore[b]
            if not found_point or danger_ignore_visited:
                break
        if not found_point:
            break

    if keep_paths:
        return weights, paths

    return weights

class Dictlike():
    """Dictlike object acts like a read-only dictionary but where
    'd[k]' and 'k in d' operations are provided by functions that can
    compute values on the fly.
    """

    def __init__(self, get_fn, contains_fn = lambda x: True):
        """Creates a Dictlike object with the provided get and contains functions"""
        self.get_fn = get_fn
        self.contains_fn = contains_fn

    def __getitem__(self, key):
        return self.get_fn(key)

    def __contains__(self, key):
        return self.contains_fn(key)
