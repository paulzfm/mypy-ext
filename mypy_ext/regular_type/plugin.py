import ast
from typing import Callable, Tuple

from automata.base.exceptions import InvalidRegexError
from automata.regex import regex as re

from mypy.options import Options
from mypy.plugin import AnalyzeTypeContext, Plugin, MethodContext
from mypy.types import Type, UnboundType, RawExpressionType, ProperType, LiteralType, Instance
from mypy_ext.regular_type import Re
from mypy_ext.regular_type.re_ops import re_starts_with
from mypy_ext.regular_type.typing import RegularType
from mypy_ext.utils import fullname_of


def analyze_type(ctx: AnalyzeTypeContext) -> Type:
    assert isinstance(
        ctx.type, UnboundType
    ), f"{ctx.type} of type {ctx.type.__class__.__name__} is not UnboundType"
    str_type = ctx.api.named_type("builtins.str", [])

    if len(ctx.type.args) != 1:
        ctx.api.fail("Re[...] expects one type argument", ctx.type)
        if len(ctx.type.args) == 0:
            return str_type

    arg = ctx.type.original_args[0]
    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
        regex = arg.value
    else:
        ctx.api.fail("Argument of Re[...] must be a regex string", arg)
        return str_type

    try:
        re.validate(regex)
    except InvalidRegexError:
        ctx.api.fail("Argument of Re[...] is not a valid regex", arg)
        return str_type

    return RegularType(str_type, regex, ctx.type.line, ctx.type.column)


IS_CONST = 1
IS_RE = 2
IS_STR = 3
IS_ERROR = 4


def try_extract(t: ProperType) -> Tuple[int, str]:
    if isinstance(t, LiteralType) and isinstance(t.value, str):
        return IS_CONST, t.value
    if isinstance(t, Instance) and t.last_known_value is not None:
        return try_extract(t.last_known_value)
    if isinstance(t, RegularType):
        return IS_RE, t.regex
    if isinstance(t, Instance) and t.type.fullname == "builtins.str":
        return IS_STR, '.*'  # the regex that matches any string

    return IS_ERROR, ''


def infer_add(ctx: MethodContext) -> Type:
    str_type = ctx.api.named_generic_type("builtins.str", [])

    t1, [[t2]] = ctx.type, ctx.arg_types
    k1, s1 = try_extract(t1)
    k2, s2 = try_extract(t2)

    if k1 == IS_CONST and k2 == IS_CONST:
        return LiteralType(s1 + s2, str_type)
    if k1 == IS_STR and k2 == IS_STR:
        return str_type
    if k1 != IS_ERROR and k2 != IS_ERROR:
        return RegularType(str_type, f"({s1})({s2})")

    # fallback
    return str_type


def infer_startswith(ctx: MethodContext) -> Type:
    bool_type = ctx.api.named_generic_type("builtins.bool", [])

    t1, [[t2], _, _] = ctx.type, ctx.arg_types
    k1, s1 = try_extract(t1)
    k2, s2 = try_extract(t2)

    if k1 == IS_CONST and k2 == IS_CONST:
        return LiteralType(s1.startswith(s2), bool_type)
    if k1 == IS_RE and k2 == IS_CONST:
        return LiteralType(re_starts_with(s1, s2), bool_type)
    if k1 == IS_RE and k2 == IS_RE:
        pass  # consider this in future

    # fallback
    return bool_type


class RegularPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)

    def get_type_analyze_hook(self, fullname: str) -> Callable[[AnalyzeTypeContext], Type] | None:
        if fullname == fullname_of(Re):
            return analyze_type

        return None

    def get_method_hook(self, fullname: str) -> Callable[[MethodContext], Type] | None:
        if fullname.endswith("of str"):  # DEBUG
            raise NotImplementedError(f"Weird name: {fullname}")

        if fullname == "builtins.str.__add__":
            return infer_add

        if fullname == "builtins.str.startswith":
            return infer_startswith

        if fullname == "builtins.str.endswith":
            return infer_startswith

        return None


def plugin(version: str):
    return RegularPlugin
