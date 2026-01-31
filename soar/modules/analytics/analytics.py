from functools import wraps
from typing import Callable

from soar.modules.analytics.db import _insert


def analytic(event_name: str):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(event):
            _insert(event_name)
            return func(event)

        return wrapper

    return decorator
