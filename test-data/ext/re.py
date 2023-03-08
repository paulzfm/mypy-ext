from typing import Literal

from mypy_ext.regular_type import Re


def re_cast() -> None:
    s1: Re["ab"] = "ab"
    s2: str = s1
    s3: Literal["hello"] = "hello"
    s4: Re["hello"] = s3
    n: int = len(s4)


def re_subtype(s: Re["a+"]) -> Re["a*"]:
    return s


def str_lit_concat(s1: Literal["a"], s2: Literal["b"]) -> Literal["ab"]:
    return s1 + s2


def re_concat(s1: Re["a+"], s2: Re["b+"]) -> Re["a+b+"]:
    return s1 + s2


def re_str_concat(s1: Re["a|b"], s2: str) -> Re["(a|b).*"]:
    return s1 + s2


def suffix_with_s(s: str) -> Re[".*s"]:
    return s + "s"


def should_start_with(s: Re["a+b+"]) -> Literal[True]:
    return s.startswith("a")


def should_end_with(s: Re["a+b+"]) -> Literal[True]:
    return s.endswith("b")


# def may_not_end_with(s: Re["a+b*"]) -> Literal[True]:
#     return s.endswith("b")   # type error
