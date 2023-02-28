from typing import Literal

from mypy_ext.finite_type import Fin


def fin_cast() -> None:
    x: Fin[10] = 9
    x1: int = x
    y: Literal[8] = 8
    y1: Fin[9] = y


def fin_10_spec(x: Fin[10]) -> None:
    assert 0 <= x < 10


def fin_subtype_test(x: Fin[9]) -> Fin[10]:
    return x


def fin_inc(x: Fin[3]) -> Fin[4]:
    return x + 1


def fin_add(x: Fin[3], y: Fin[10]) -> Fin[13]:
    return x + y
