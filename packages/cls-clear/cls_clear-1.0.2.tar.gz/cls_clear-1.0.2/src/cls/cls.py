"""Module for terminal clearing in interactive mode."""

import sys
from threading import Timer

if not bool(getattr(sys, "ps1", sys.flags.interactive)):
    msg = "This module can only be used in interactive mode."
    raise ImportError(msg)


class _Clearer:
    # Simple class to clear the terminal
    _ps1 = str(sys.ps1)

    def __repr__(self) -> str:
        # Cannot clear directly here as the prompt will be in a new line.
        # Also, decorating the function won't work as the result will not
        # be displayed immediately but rather stored; tough luck.
        Timer(0.001, self._clear).start()
        return ""

    def _clear(self) -> None:
        """Clear the terminal and emit python's REPL prompt."""
        sys.stdout.write("\x1b[2J\x1b[H{}".format(self._ps1))
        sys.stdout.flush()

    def __call__(self) -> None:
        self._clear()


cls = _Clearer()
clear = _Clearer()
del _Clearer
