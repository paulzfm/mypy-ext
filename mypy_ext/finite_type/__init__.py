from typing import TypeVar, Generic

N = TypeVar("N")


class Fin(Generic[N]):
    def __add__(self, other):
        pass
