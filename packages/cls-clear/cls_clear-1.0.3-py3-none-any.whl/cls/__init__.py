"""Clear the screen in the interactive mode Python."""

import inspect

from .cls import clear, cls

__version__ = "1.0.3"

__all__ = ["__version__", "clear", "cls"]


def _init() -> None:
    # Inject the two instances into the caller's locals
    stack = inspect.stack()
    try:
        caller_locals = stack[-1][0].f_locals
    finally:
        del stack

    caller_locals["cls"] = cls
    caller_locals["clear"] = clear


_init()
