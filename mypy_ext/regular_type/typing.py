from typing import Sequence

from automata.base.exceptions import InvalidRegexError
from automata.fa.nfa import NFA
from automata.regex import regex as re

from mypy.plugin import TypeAnalyzerPluginInterface
from mypy.types import Instance, JsonDict, LiteralValue, RefinementType, Type, LiteralType
from mypy_ext.regular_type import Re
from mypy_ext.utils import fullname_of, type_is, RefinementTypeBuilder


class RegularType(RefinementType):
    fullname = fullname_of(Re)
    name = Re.__name__

    regex: str

    def __init__(self, base: Instance, regex: str, line: int = -1, column: int = -1) -> None:
        """Assume the input regex is valid."""
        # assert base.type.fullname == "builtins.str"
        super().__init__(base, line, column)
        self.regex = regex

    def args_repr(self) -> Sequence[str]:
        return [self.regex]

    def shallow_copy(self) -> RefinementType:
        return RegularType(self.base, self.regex, self.line, self.column)

    def __le__(self, other: Type) -> bool:
        if isinstance(other, RegularType):
            if self.regex == other.regex:
                return True
            return re.issubset(self.regex, other.regex)
        if type_is(other, "typing.Sized"):
            return True
        if isinstance(other, LiteralType) and isinstance(other.value, str):
            return re.isequal(self.regex, other.value)

        return False

    def __contains__(self, value: LiteralValue) -> bool:
        if isinstance(value, str):
            nfa = NFA.from_regex(self.regex)
            return nfa.accepts_input(value)
        return False

    def serialize_args(self) -> JsonDict | str:
        return self.regex

    @classmethod
    def deserialize_args(cls, base: Instance, args: JsonDict | str) -> Type:
        assert isinstance(args, str)
        return RegularType(base, args)


class RegularTypeBuilder(RefinementTypeBuilder):
    def __init__(self, regex: str):
        self.regex = regex

    def build(self, api: TypeAnalyzerPluginInterface, line: int = -1, column: int = -1) -> Type:
        str_type = api.named_type("builtins.str", [])
        re.validate(self.regex)
        return RegularType(str_type, self.regex, line, column)


def re_lang(regex: str) -> RefinementTypeBuilder:
    return RegularTypeBuilder(regex)
