import functools
import logging
from typing import Any, Callable, Optional, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def disney_property(refresh: bool = True, default_value: Optional[T] = None) -> Callable:
    def decorator(func: Callable) -> property:
        @property
        @functools.wraps(func)
        def wrapper(self) -> Optional[T]:
            if refresh:
                self.refresh()
            try:
                return func(self)
            except (KeyError, TypeError, ValueError):
                return default_value

        return wrapper

    return decorator


def json_property(func: Callable) -> property:
    @property
    @functools.wraps(func)
    def wrapper(self) -> Any:
        try:
            return func(self)
        except (KeyError, TypeError, ValueError):
            return None

    return wrapper
