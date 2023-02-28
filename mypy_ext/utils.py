from __future__ import annotations

from typing import Type as PyType

from mypy.types import Type, Instance


def fullname_of(x: PyType) -> str:
    return ".".join([x.__module__, x.__name__])


def type_is(t: Type, fullname: str) -> bool:
    return isinstance(t, Instance) and t.type.fullname == fullname
