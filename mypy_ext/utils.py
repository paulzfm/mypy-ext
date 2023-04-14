from __future__ import annotations

from abc import abstractmethod
from typing import Type as PyType

from mypy.plugin import TypeAnalyzerPluginInterface
from mypy.types import Instance, Type


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


class RefinementTypeBuilder:
    @abstractmethod
    def build(self, api: TypeAnalyzerPluginInterface, line: int = -1, column: int = -1) -> Type:
        pass
