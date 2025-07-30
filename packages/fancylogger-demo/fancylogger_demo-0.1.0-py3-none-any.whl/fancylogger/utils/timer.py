import time
from functools import wraps

def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[log_time] '{func.__name__}' took {end - start:.4f}s")
        return result
    return wrapper
