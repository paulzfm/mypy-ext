from typing import Generic, TypeVar

from mypy.typing_extension import Refinable

T = TypeVar("T")
N = TypeVar("N")


class Vec(Refinable, Generic[T, N]):
    pass
