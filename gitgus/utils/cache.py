import json
import os
import pickle
import time
from typing import Generator

MAX_CACHE_MINUTES = 5
DEFAULT_CACHE_PATH = os.path.join(os.path.expanduser("~"), ".cache", "gitgus")

global_cache_enabled = True


def persist_to_file():
    def decorator(original_func):
        file_name = os.path.join(
            DEFAULT_CACHE_PATH,
            original_func.__module__ + original_func.__name__ + ".pkl",
        )
        cache = {}

        # Is the cache file older too old?
        if os.path.exists(file_name):
            if (time.time() - os.path.getmtime(file_name)) / 60 > MAX_CACHE_MINUTES:
                os.remove(file_name)

            try:
                # unpickle the cache
                cache = pickle.load(open(file_name, "rb"))
            except (IOError, ValueError, EOFError):
                cache = {}
        else:
            os.makedirs(os.path.dirname(file_name), exist_ok=True)

        def new_func(s, *args, **kwargs):
            key = str(args) + str(kwargs)
            if key not in cache or not global_cache_enabled:
                res = original_func(s, *args, **kwargs)
                if isinstance(res, Generator):
                    res = list(res)
                cache[key] = res
                pickle.dump(cache, open(file_name, "wb"))
            return cache[key]

        return new_func

    return decorator
