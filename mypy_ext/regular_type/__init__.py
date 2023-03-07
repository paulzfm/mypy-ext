from typing import Generic, TypeVar

from mypy.typing_extension import Refinable

R = TypeVar("R")


class Re(Refinable, Generic[R]):
    pass
