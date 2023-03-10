import ast
from typing import Callable

from automata.base.exceptions import InvalidRegexError

from mypy.options import Options
from mypy.plugin import AnalyzeTypeContext, MethodContext, Plugin, FunctionContext
from mypy.types import Instance, LiteralType, ProperType, Type, UnboundType
from mypy_ext.finite_type.plugin import try_extract as try_extract_int
from mypy_ext.regular_type import Re
from mypy_ext.regular_type.re_ops import *
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
        RE.validate(regex)
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
        return IS_STR, ".*"  # the regex that matches any string

    return IS_ERROR, ""


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


def infer_length(ctx: FunctionContext) -> Type:
    int_type = ctx.api.named_generic_type("builtins.int", [])

    [[t]] = ctx.arg_types
    k, s = try_extract(t)

    if k == IS_CONST:
        return LiteralType(len(s), int_type)
    if k == IS_RE:
        minimal, maximal = re_length(s)
        if maximal is not None and minimal == maximal:
            return LiteralType(minimal, int_type)

    # fallback
    return int_type


def infer_startswith(ctx: MethodContext) -> Type:
    bool_type = ctx.api.named_generic_type("builtins.bool", [])

    t1, [[t2], _, _] = ctx.type, ctx.arg_types
    k1, s1 = try_extract(t1)
    k2, s2 = try_extract(t2)

    if k1 == IS_CONST and k2 == IS_CONST:
        return LiteralType(s1.startswith(s2), bool_type)
    if k1 == IS_RE and k2 == IS_CONST and re_starts_with(s1, s2):
        return LiteralType(True, bool_type)
    if k1 == IS_RE and k2 == IS_RE and re_starts_with_re(s1, s2):
        return LiteralType(True, bool_type)

    # fallback
    return bool_type


def infer_endswith(ctx: MethodContext) -> Type:
    bool_type = ctx.api.named_generic_type("builtins.bool", [])

    t1, [[t2], _, _] = ctx.type, ctx.arg_types
    k1, s1 = try_extract(t1)
    k2, s2 = try_extract(t2)

    if k1 == IS_CONST and k2 == IS_CONST:
        return LiteralType(s1.startswith(s2), bool_type)
    if k1 == IS_RE and k2 == IS_CONST and re_ends_with(s1, s2):
        return LiteralType(True, bool_type)
    if k1 == IS_RE and k2 == IS_RE and re_ends_with_re(s1, s2):
        return LiteralType(True, bool_type)

    # fallback
    return bool_type


def infer_contains(ctx: MethodContext) -> Type:
    bool_type = ctx.api.named_generic_type("builtins.bool", [])

    t1, [[t2]] = ctx.type, ctx.arg_types
    k1, s1 = try_extract(t1)
    k2, s2 = try_extract(t2)

    if k1 == IS_CONST and k2 == IS_CONST:
        return LiteralType(s1 in s2, bool_type)
    if k1 == IS_RE and k2 == IS_CONST and re_contains(s1, s2):
        return LiteralType(True, bool_type)
    if k1 == IS_RE and k2 == IS_RE and re_contains_re(s1, s2):
        return LiteralType(True, bool_type)

    # fallback
    return bool_type


def infer_upper(ctx: MethodContext) -> Type:
    str_type = ctx.api.named_generic_type("builtins.str", [])
    t, [] = ctx.type, ctx.arg_types
    k, s = try_extract(t)

    if k == IS_CONST:
        return LiteralType(s.upper(), str_type)
    if k == IS_RE:
        regex = s.upper()
        assert RE.validate(regex)
        return RegularType(str_type, regex)
    return str_type


def infer_lower(ctx: MethodContext) -> Type:
    str_type = ctx.api.named_generic_type("builtins.str", [])
    t, [] = ctx.type, ctx.arg_types
    k, s = try_extract(t)

    if k == IS_CONST:
        return LiteralType(s.lower(), str_type)
    if k == IS_RE:
        regex = s.lower()
        assert RE.validate(regex)
        return RegularType(str_type, regex)
    return str_type


def infer_get_item(ctx: MethodContext) -> Type:
    str_type = ctx.api.named_generic_type("builtins.str", [])
    t, [[ti]] = ctx.type, ctx.arg_types
    k, s = try_extract(t)
    ki, n = try_extract_int(ti)

    if k == IS_CONST and ki == IS_CONST:
        return LiteralType(s[n], str_type)
    if k == IS_RE and ki == IS_CONST:
        minimal, _ = re_length(s)
        if n >= minimal:
            ctx.api.fail(f"Index out of range (minimal length is {minimal})", ctx.context)
            return str_type
        return RegularType(str_type, re_char_at(s, n + 1))

    # fallback
    return str_type


class RegularPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)

    def get_type_analyze_hook(self, fullname: str) -> Callable[[AnalyzeTypeContext], Type] | None:
        if fullname == fullname_of(Re):
            return analyze_type

        return None

    def get_function_hook(self, fullname: str) -> Callable[[FunctionContext], Type] | None:
        if fullname == "builtins.len":
            return infer_length

        return None

    def get_method_hook(self, fullname: str) -> Callable[[MethodContext], Type] | None:
        if fullname.endswith("of str"):  # DEBUG
            raise NotImplementedError(f"Weird name: {fullname}")

        if fullname == "builtins.str.__add__":
            return infer_add

        if fullname == "builtins.str.startswith":
            return infer_startswith

        if fullname == "builtins.str.endswith":
            return infer_endswith

        if fullname == "builtins.str.__contains__":
            return infer_contains

        if fullname == "builtins.str.upper":
            return infer_upper

        if fullname == "builtins.str.lower":
            return infer_lower

        if fullname == "builtins.str.__getitem__":
            return infer_get_item

        return None


def plugin(version: str):
    return RegularPlugin
