from typing import cast, Callable

from fuzzingbook.Grammars import is_valid_grammar

from mypy.options import Options
from mypy.plugin import AnalyzeRefinementTypeContext, Plugin
from mypy.types import Type
from mypy_ext.lang_type import LangTypeWrapper
from mypy_ext.lang_type.typing import LangType
from mypy_ext.utils import fullname_of


def analyze_refinement_type(ctx: AnalyzeRefinementTypeContext) -> Type:
    wrapper = cast(LangTypeWrapper, ctx.wrapper)
    str_type = ctx.api.named_type("builtins.str", [])

    if not is_valid_grammar(wrapper.grammar):
        ctx.api.fail("Argument of lang(...) is not a valid grammar", ctx.context)
        return str_type

    return LangType(str_type, wrapper.grammar, wrapper.name, ctx.context.line, ctx.context.column)


class LangPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)

    def get_refinement_type_analyze_hook(self, fullname: str) -> Callable[[AnalyzeRefinementTypeContext], Type] | None:
        if fullname == fullname_of(LangTypeWrapper):
            return analyze_refinement_type

        return None


def plugin(version: str):
    return LangPlugin
