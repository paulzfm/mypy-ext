from __future__ import annotations

from typing import Callable, Tuple

from mypy.options import Options
from mypy.plugin import AnalyzeTypeContext, MethodContext, Plugin
from mypy.types import Instance, LiteralType, ProperType, RawExpressionType, Type, UnboundType
from mypy_ext.finite_type import Fin
from mypy_ext.finite_type.typing import FiniteType
from mypy_ext.utils import fullname_of


def analyze_type(ctx: AnalyzeTypeContext) -> Type:
    assert isinstance(
        ctx.type, UnboundType
    ), f"{ctx.type} of type {ctx.type.__class__.__name__} is not UnboundType"
    int_type = ctx.api.named_type("builtins.int", [])

    if len(ctx.type.args) != 1:
        ctx.api.fail("Fin[...] expects one type argument", ctx.type)
        if len(ctx.type.args) == 0:
            return int_type

    arg = ctx.type.args[0]
    if not isinstance(arg, RawExpressionType) or not isinstance(arg.literal_value, int):
        ctx.api.fail("Argument of Fin[...] must be an integer literal", arg)
        return int_type

    bound = arg.literal_value
    if bound <= 0:
        ctx.api.fail("Argument of Fin[...] must be a positive integer", arg)
        return int_type

    return FiniteType(int_type, bound, ctx.type.line, ctx.type.column)


IS_CONST = 1
IS_FIN = 2
IS_ERROR = 3


def try_extract(t: ProperType) -> Tuple[int, int]:
    if isinstance(t, LiteralType) and isinstance(t.value, int):
        return IS_CONST, t.value
    if isinstance(t, Instance) and t.last_known_value is not None:
        return try_extract(t.last_known_value)
    if isinstance(t, FiniteType):
        return IS_FIN, t.bound

    return IS_ERROR, -1


def check_add(ctx: MethodContext) -> Type:
    int_type = ctx.api.named_generic_type("builtins.int", [])

    t1, [[t2]] = ctx.type, ctx.arg_types
    k1, n1 = try_extract(t1)
    k2, n2 = try_extract(t2)

    if k1 == IS_CONST and k2 == IS_CONST:
        return LiteralType(n1 + n2, int_type)
    if k1 != IS_ERROR and k2 != IS_ERROR:
        return FiniteType(int_type, n1 + n2)

    # fallback
    return int_type


class FinitePlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)

    def get_type_analyze_hook(self, fullname: str) -> Callable[[AnalyzeTypeContext], Type] | None:
        if fullname == fullname_of(Fin):
            return analyze_type

        return None

    def get_method_hook(self, fullname: str) -> Callable[[MethodContext], Type] | None:
        if fullname.endswith("of int"):  # DEBUG
            raise NotImplementedError(f"Weird name: {fullname}")

        if fullname == "builtins.int.__add__":
            return check_add

        return None


def plugin(version: str):
    return FinitePlugin
