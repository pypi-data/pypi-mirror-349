from typing import (
    Any, Callable
)

class matcher:
    def __init__(self, value: Any, func: Callable[[Any, Any], Any], matches: list[Any, Any], default=None, *args, **kwargs):
        self.value = value
        self.func = func
        self.matches = matches
        self.default = default
        self._args = args
        self._kwargs = kwargs

    def __str__(self):
        for match in self.matches:
            if self.func(self.value, match[0]):
                m = match[1]
                if callable(m):
                    return m(*self._args, **self._kwargs)
                return m
            
        return self.default
