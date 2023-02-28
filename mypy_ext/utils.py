from __future__ import annotations

from typing import Type


def fullname_of(x: Type) -> str:
    return '.'.join([x.__module__, x.__name__])
