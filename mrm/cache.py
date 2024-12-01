"""Module for customizable caching decorator"""

__all__ = ['Keycache']

import functools

class Keycache:
    """Provides a decorator for caching return values based on a customizable key
    instead of all function parameters and which can provide debug stats and resets
    """

    def __init__(self, stats=False):
        """Stats and resets will only be available if stats=True"""
        self._stats = stats
    
    class KeycacheWithStats:
        def __init__(self, fn):
            """Sets up wrapped version of function with caching and stats/resets
            fn must have a kwarg named key
            """

            self._cache = {}
            self._hits = 0
            self._misses = 0
            @functools.wraps(fn)
            def _cached_fn(*args, **kwargs):
                k = kwargs['key']
                if k not in self._cache:
                    self._misses += 1
                    v = fn(*args, **kwargs)
                    self._cache[k] = v
                else:
                    self._hits += 1
                    v = self._cache[k]
                return v
            self._cached_fn = _cached_fn

        def __call__(self, *args, **kwargs):
            """Calls wrapped function"""
            return self._cached_fn(*args, **kwargs)

        def stats(self):
            """Returns cache hits and misses experienced since init/reset"""
            return self._hits, self._misses

        def reset(self, stats_only=False):
            """Resets hits/misses stats and optionally the cache as well"""
            if not stats_only:
                self._cache = {}
            self._hits = 0
            self._misses = 0

    def __call__(self, fn):
        """Returns wrapped version of function with caching
        fn must have a kwarg named key
        """

        if not self._stats:
            cache = {}
            @functools.wraps(fn)
            def _cached_fn(*args, **kwargs):
                k = kwargs['key']
                if k not in cache:
                    v = fn(*args, **kwargs)
                    cache[k] = v
                else:
                    v = cache[k]
                return v
            return _cached_fn
        return self.KeycacheWithStats(fn)
