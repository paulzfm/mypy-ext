# concat
from typing import Literal

from mypy_ext.regular_type import Re


def str_lit_concat(s1: Literal["a"], s2: Literal["b"]) -> Literal["ab"]:
    return s1 + s2


def re_concat(s1: Re["a+"], s2: Re["b+"]) -> Re["a+b+"]:
    return s1 + s2


def re_str_concat(s1: Re["a|b"], s2: str) -> Re["(a|b).*"]:
    return s1 + s2


def suffix_with_s(s: str) -> Re[".*s"]:
    return s + "s"


# startswith, endswith
def should_start_with_a(s: Re["a+b+"]) -> Literal[True]:
    return s.startswith("a")


def should_end_with_b(s: Re["a+b+"]) -> Literal[True]:
    return s.endswith("b")


# def may_not_end_with_b(s: Re["a+b*"]) -> Literal[True]:
#     return s.endswith("b")  # type error
