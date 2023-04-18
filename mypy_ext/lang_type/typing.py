from typing import Sequence

from fuzzingbook.Grammars import Grammar
from fuzzingbook.Parser import EarleyParser

from mypy.types import RefinementType, Instance, Type, LiteralValue, JsonDict
from mypy_ext.lang_type import lang
from mypy_ext.utils import fullname_of, type_is


class LangType(RefinementType):
    fullname = fullname_of(lang)
    name = lang.__name__

    grammar: Grammar

    def __init__(self, base: Instance, grammar: Grammar, tag: str, line: int = -1, column: int = -1) -> None:
        """Assume the input grammar is valid."""
        # assert base.type.fullname == "builtins.str"
        super().__init__(base, line, column)
        self.grammar = grammar
        self.tag = tag

    def args_repr(self) -> Sequence[str]:
        return [self.tag]

    def shallow_copy(self) -> RefinementType:
        return LangType(self.base, self.grammar, self.tag, self.line, self.column)

    def __le__(self, other: Type) -> bool:
        if isinstance(other, LangType):
            if self.grammar == other.grammar:
                return True
            return False  # TODO: sub lang
        if type_is(other, "typing.Sized"):
            return True

        return False

    def __contains__(self, value: LiteralValue) -> bool:
        if isinstance(value, str):
            parser = EarleyParser(self.grammar)
            try:
                next(parser.parse(value))
            except SyntaxError:
                return False
            else:
                return True

        return False

    def serialize_args(self) -> JsonDict | str:
        return {
            'grammar': self.grammar,
            'tag': self.tag
        }

    @classmethod
    def deserialize_args(cls, base: Instance, args: JsonDict | str) -> Type:
        assert isinstance(args, JsonDict)
        return LangType(base, args['grammar'], args['tag'])
