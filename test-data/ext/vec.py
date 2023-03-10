from typing import Literal, TypeVar

from mypy_ext.finite_type import Fin
from mypy_ext.vector_type import Vec


def vec_to_list(v: Vec[int, 10]) -> list[int]:
    return v


class Shape:
    pass


class Square(Shape):
    pass


def vec_to_list_up_cast(v: Vec[Square, 10]) -> list[Shape]:
    return v


def vec_subtype(v: Vec[Square, 5]) -> Vec[Shape, 5]:
    return v


def vec_length(v: Vec[Shape, 5]) -> Literal[5]:
    # TODO: it seems that multiple plugins have conflict in hooking the same method
    return len(v)


def vec_get(v: Vec[Shape, 5], i: Fin[5]) -> Shape:
    return v[i]


def vec_set(v: Vec[Shape, 5], i: Fin[5], x: Shape) -> None:
    v[i] = x


def vec_get_set_by_index(v: Vec[Shape, 5]) -> None:
    s = v[4]
    v[0] = s
    # v[5] = s  # type error


T = TypeVar("T")


def vec_concat(v1: Vec[T, 10], v2: Vec[T, 5]) -> Vec[T, 15]:
    return v1 + v2
