import functools
from typing import Any, Callable


def metric(column_rename: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            result = result.rename({kwargs["column_name"]: column_rename})
            return result

        wrapper.__metric__ = True
        return wrapper

    return decorator
