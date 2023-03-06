from typing import Sequence

from automata.regex import regex as re
from automata.fa.nfa import NFA

from mypy.types import RefinementType, JsonDict, Type, LiteralValue, Instance
from mypy_ext.regular_type import Re
from mypy_ext.utils import fullname_of, type_is


class RegularType(RefinementType):
    fullname = fullname_of(Re)
    name = Re.__name__

    regex: str

    def __init__(self, base: Instance, regex: str, line: int = -1, column: int = -1) -> None:
        """Assume the input regex is valid."""
        assert base.type.fullname == "builtins.str"
        super().__init__(base, line, column)
        self.regex = regex

    def args_repr(self) -> Sequence[str]:
        return [self.regex]

    def shallow_copy(self) -> RefinementType:
        return RegularType(self.base, self.regex, self.line, self.column)

    def __le__(self, other: Type) -> bool:
        if isinstance(other, RegularType):
            print(f"{self.regex} <:? {other.regex}")
            return re.issubset(self.regex, other.regex)
        if type_is(other, "typing.Sized"):
            return True
        return False

    def __contains__(self, value: LiteralValue) -> bool:
        if isinstance(value, str):
            nfa = NFA.from_regex(self.regex)
            return nfa.accepts_input(value)
        return False

    def serialize(self) -> JsonDict | str:
        return {".class": "RegularType", "base": self.base.serialize(), "regex": self.regex}

    @classmethod
    def deserialize(cls, data: JsonDict) -> Type:
        assert data[".class"] == "RegularType"
        base = Instance.deserialize(data["base"])
        regex: str = data["regex"]
        return RegularType(base, regex)
