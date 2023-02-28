from typing import Generic, TypeVar

N = TypeVar("N")


class Fin(Generic[N]):
    def __add__(self, other):
        pass
