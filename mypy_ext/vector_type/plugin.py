from __future__ import annotations

from typing import Callable

from mypy.join import join_types
from mypy.options import Options
from mypy.plugin import (
    AnalyzeTypeContext,
    FunctionContext,
    MethodContext,
    MethodSigContext,
    Plugin,
)
from mypy.types import FunctionLike, Instance, LiteralType, RawExpressionType, Type, UnboundType
from mypy_ext.finite_type.typing import FiniteType
from mypy_ext.utils import fullname_of
from mypy_ext.vector_type import Vec
from mypy_ext.vector_type.typing import VectorType


def analyze_type(ctx: AnalyzeTypeContext) -> Type:
    assert isinstance(
        ctx.type, UnboundType
    ), f"{ctx.type} of type {ctx.type.__class__.__name__} is not UnboundType"

    if len(ctx.type.args) != 2:
        ctx.api.fail("Vec[...] expects two type arguments", ctx.type)
        if len(ctx.type.args) < 1:
            return ctx.api.named_type("builtins.list", [])

    elem_type = ctx.api.analyze_type(ctx.type.args[0])
    list_type = ctx.api.named_type("builtins.list", [elem_type])

    arg = ctx.type.args[1]
    if not isinstance(arg, RawExpressionType) or not isinstance(arg.literal_value, int):
        ctx.api.fail("Argument 2 of Vec[...] must be an integer literal", arg)
        return list_type

    size = arg.literal_value
    if size < 0:
        ctx.api.fail("Argument 2 of Vec[...] must be a non-negative integer", arg)
        return list_type

    return VectorType(list_type, elem_type, size, ctx.type.line, ctx.type.column)


def infer_len(ctx: FunctionContext) -> Type:
    [[t]] = ctx.arg_types
    if isinstance(t, VectorType):
        assert isinstance(ctx.default_return_type, Instance)
        assert ctx.default_return_type.type.fullname == "builtins.int"
        return LiteralType(t.size, ctx.default_return_type)

    return ctx.default_return_type


def infer_add(ctx: MethodContext) -> Type:
    t1, [[t2]] = ctx.type, ctx.arg_types
    if isinstance(t1, VectorType) and isinstance(t2, VectorType):
        lub = join_types(t1.elem_type, t2.elem_type)
        return VectorType(t1.base, lub, t1.size + t2.size)

    return ctx.default_return_type


def check_get_set(ctx: MethodSigContext) -> FunctionLike:
    sig = ctx.default_signature
    if isinstance(ctx.type, VectorType):
        sig.arg_types[0] = FiniteType(
            ctx.api.named_generic_type("builtins.int", []), ctx.type.size
        )

    return sig


class VectorPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)

    def get_type_analyze_hook(self, fullname: str) -> Callable[[AnalyzeTypeContext], Type] | None:
        if fullname == fullname_of(Vec):
            return analyze_type

        return None

    def get_function_hook(self, fullname: str) -> Callable[[FunctionContext], Type] | None:
        if fullname == "builtins.len":
            return infer_len

        return None

    def get_method_signature_hook(
        self, fullname: str
    ) -> Callable[[MethodSigContext], FunctionLike] | None:
        if fullname in ("builtins.list.__getitem__", "builtins.list.__setitem__"):
            return check_get_set

        return None

    def get_method_hook(self, fullname: str) -> Callable[[MethodContext], Type] | None:
        if fullname.endswith("of list"):  # DEBUG
            raise NotImplementedError(f"Weird name: {fullname}")

        if fullname == "builtins.list.__add__":
            return infer_add

        return None


def plugin(version: str):
    return VectorPlugin
