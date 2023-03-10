from typing import Literal

from mypy_ext.regular_type import Re


# concat
def str_lit_concat(s1: Literal["a"], s2: Literal["b"]) -> Literal["ab"]:
    return s1 + s2


def re_concat(s1: Re["a+"], s2: Re["b+"]) -> Re["a+b+"]:
    return s1 + s2


def re_str_concat(s1: Re["a|b"], s2: str) -> Re["(a|b).*"]:
    return s1 + s2


def suffix_with_s(s: str) -> Re[".*s"]:
    return s + "s"


# length
def re_fixed_length(s: Re["(a|b)(c|d)"]) -> Literal[2]:
    return len(s)


def re_length_not_fixed(s: Re["a+"]) -> int:
    return len(s)


# startswith, endswith
def should_start_with_a(s: Re["a+b+"]) -> Literal[True]:
    return s.startswith("a")


def should_start_with_a_plus(s: Re["a+b+"], s1: Re["a+"]) -> Literal[True]:
    return s.startswith(s1)


def should_end_with_b(s: Re["a+b+"]) -> Literal[True]:
    return s.endswith("b")


def should_end_with_b_plus(s: Re["a+b+"], s1: Re["b+"]) -> Literal[True]:
    return s.endswith(s1)


def may_not_end_with_b(s: Re["a+b*"]) -> bool:
    return s.endswith("b")


# __contains__
def should_contain_a(s: Re["a+b+"]) -> Literal[True]:
    return "a" in s


def should_contain_ab(s: Re["a+b+"]) -> Literal[True]:
    return "ab" in s


# upper, lower
def re_to_upper(s: Re["a+b+"]) -> Re["A+B+"]:
    return s.upper()


def re_to_lower(s: Re["A+b+"]) -> Re["a+b+"]:
    return s.lower()


# __getitem__
def re_getitem_det(s: Re["a+b+"]) -> Literal["a"]:
    return s[0]


def re_getitem_nondet(s: Re["a+b+"]) -> Re["a|b"]:
    return s[1]


def re_getitem_out_of_bound(s: Re["a+b+"]) -> str:
    return s[2]  # type error
