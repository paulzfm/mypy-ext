from __future__ import annotations

from typing import Type as PyType, TypeVar, Generic

from mypy.types import Type, Instance


def fullname_of(x: PyType) -> str:
    return ".".join([x.__module__, x.__name__])


def type_is(t: Type, fullname: str) -> bool:
    return isinstance(t, Instance) and t.type.fullname == fullname


def flat_map(f, xs):
    ys = []
    for x in xs:
        ys.extend(f(x))
    return ys


def union_map(f, xs):
    ys = set()
    for x in xs:
        ys.update(f(x))
    return ys
