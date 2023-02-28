from __future__ import annotations

from mypy.types import RefinementType, JsonDict, Type, LiteralValue, Instance


class FiniteType(RefinementType):
    bound: int

    def __init__(self, base: Instance, bound: int, line: int = -1, column: int = -1) -> None:
        assert base.type.fullname == "builtins.int"
        super().__init__(base, line, column)
        self.bound = bound

    def type_repr(self) -> str:
        return f'Fin[{self.bound}]'

    def shallow_copy(self) -> RefinementType:
        return FiniteType(self.base, self.bound, self.line, self.column)

    def __le__(self, other: Type) -> bool:
        if isinstance(other, FiniteType):
            return self.bound <= other.bound

    def __contains__(self, value: LiteralValue) -> bool:
        if isinstance(value, int):
            return 0 <= value < self.bound
        return False

    def serialize(self) -> JsonDict | str:
        return {
            ".class": "FiniteType",
            "base": self.base.serialize(),
            "bound": self.bound,
        }

    @classmethod
    def deserialize(cls, data: JsonDict) -> Type:
        assert data[".class"] == "FiniteType"
        base = Instance.deserialize(data["base"])
        bound: int = data["bound"]
        return FiniteType(base, bound)
