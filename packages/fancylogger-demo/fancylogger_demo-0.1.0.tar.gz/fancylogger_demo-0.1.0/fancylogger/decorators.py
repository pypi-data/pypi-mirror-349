from functools import wraps
from fancylogger.utils.timer import log_time

def log_io(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[log_io] Calling '{func.__name__}' with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[log_io] Result from '{func.__name__}': {result}")
        return result
    return wrapper

def log_all(func):
    @log_io
    @log_time
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
