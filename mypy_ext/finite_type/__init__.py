from typing import Generic, TypeVar

from mypy.typing_extension import Refinable

N = TypeVar("N")


class Fin(Refinable, Generic[N]):
    pass
