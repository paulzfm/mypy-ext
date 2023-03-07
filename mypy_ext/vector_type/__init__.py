from typing import TypeVar, Generic

from mypy.typing_extension import Refinable1

T = TypeVar("T")
N = TypeVar("N")


class Vec(Refinable1, Generic[T, N]):
    pass
