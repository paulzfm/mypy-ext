from typing import Literal

from mypy_ext.finite_type import Fin


def int_inc(x: int) -> int:
    return x + 1


def fin_cast() -> None:
    x: Fin[10] = 9
    x1: int = x
    y: Literal[8] = 8
    y1: Fin[9] = y
    int_inc(y1)


def fin_subtype(x: Fin[9]) -> Fin[10]:
    return x


def fin_inc(x: Fin[3]) -> Fin[4]:
    return x + 1


def fin_add(x: Fin[3], y: Fin[10]) -> Fin[13]:
    return x + y


def fin_call() -> None:
    x = fin_inc(2)
    # fin_add(x, x)   # type error
    y = fin_subtype(x)
    fin_add(1, y)
    # fin_add(2, -1)  # type error


def fin_as_index(xs: list[int]) -> int:
    three = fin_inc(2)
    return xs[three]
