# functools.py
# Import modules
import time

# Cache a function result
def cache(func):
    cache_dict = {}

    def make_hashable(obj):
        if isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        if isinstance(obj, tuple):
            return tuple(make_hashable(item) for item in obj)
        if isinstance(obj, list):
            return tuple(make_hashable(item) for item in obj)
        if isinstance(obj, set):
            return frozenset(make_hashable(item) for item in obj)
        if isinstance(obj, dict):
            return tuple(sorted((make_hashable(k), make_hashable(v)) for k, v in obj.items()))
        return str(obj)

    def wrapper(*args, **kwargs):
        key = make_hashable((args, kwargs))
        if key in cache_dict:
            return cache_dict[key]
        result = func(*args, **kwargs)
        cache_dict[key] = result
        return result

    return wrapper

# Measure execution time
def timer(func):
    # Decorator
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        needed_time = end_time - start_time
        return needed_time, result
    return wrapper

# Run a function n times
def run(func, n=1):
    for i in range(n):
        func()

# Retry a function
def retry(func, n=3):
    for i in range(n):
        try:
            return func()
        except:
            pass