from typing import Sequence

from mypy.subtypes import is_subtype
from mypy.types import Type, RefinementType, Instance, JsonDict, LiteralValue, deserialize_type
from mypy_ext.utils import fullname_of, type_is
from mypy_ext.vector_type import Vec


class VectorType(RefinementType):
    fullname = fullname_of(Vec)
    name = Vec.__name__

    elem_type: Type
    size: int

    def __init__(self, base: Instance, elem_type: Type, size: int, line: int = -1, column: int = -1) -> None:
        assert base.type.fullname == "builtins.list"
        super().__init__(base, line, column)
        self.elem_type = elem_type
        self.size = size

    def args_repr(self) -> Sequence[str]:
        return [repr(self.elem_type), repr(self.size)]

    def shallow_copy(self) -> RefinementType:
        return VectorType(self.base, self.elem_type, self.size, self.line, self.column)

    def __le__(self, other: Type) -> bool:
        if isinstance(other, VectorType):
            return self.size == other.size and is_subtype(self.elem_type, other.elem_type)
        if isinstance(other, Instance) and other.type.fullname == "builtins.list":
            return is_subtype(self.elem_type, other.args[0])
        if type_is(other, "typing.Sized"):
            return True

        return False

    def __contains__(self, value: LiteralValue) -> bool:
        return False

    def serialize(self) -> JsonDict | str:
        return {".class": "VectorType", "base": self.base.serialize(),
                "elem_type": self.elem_type.serialize(), "size": self.size}

    @classmethod
    def deserialize(cls, data: JsonDict) -> Type:
        assert data[".class"] == "VectorType"
        base = Instance.deserialize(data["base"])
        elem_type = deserialize_type(data["elem_type"])
        size: int = data["size"]
        return VectorType(base, elem_type, size)
