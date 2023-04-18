from mypy.typing_extension import RefinementTypeWrapper
from fuzzingbook.Grammars import Grammar


class LangTypeWrapper(RefinementTypeWrapper):
    grammar: Grammar
    name: str

    def __init__(self, grammar: Grammar, name: str):
        self.grammar = grammar
        self.name = name


def lang(grammar: Grammar, name: str) -> LangTypeWrapper:
    return LangTypeWrapper(grammar, name)
