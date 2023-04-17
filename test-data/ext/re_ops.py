from typing import Literal

from re_types import *


# concat
def str_lit_concat(s1: Literal["a"], s2: Literal["b"]) -> Literal["ab"]:
    return s1 + s2


def re_concat(s1: re_lang("a+"), s2: re_lang("b+")) -> re_lang("a+b+"):
    return s1 + s2


def re_str_concat(s1: re_lang("a|b"), s2: str) -> re_lang("(a|b).*"):
    return s1 + s2


def suffix_with_s(s: re_lang("a+")) -> re_lang("a+s"):
    return s + "s"


# length
def re_fixed_length(s: re_lang("(a|b)(c|d)")) -> Literal[2]:
    return len(s)


def re_length_not_fixed(s: re_lang("a+")) -> int:
    return len(s)


# startswith, endswith
def should_start_with_a(s: re_lang("a+b+")) -> Literal[True]:
    return s.startswith("a")


def should_start_with_a_plus(s: re_lang("a+b+"), s1: re_lang("a+")) -> Literal[True]:
    return s.startswith(s1)


def should_end_with_b(s: re_lang("a+b+")) -> Literal[True]:
    return s.endswith("b")


def should_end_with_b_plus(s: re_lang("a+b+"), s1: re_lang("b+")) -> Literal[True]:
    return s.endswith(s1)


def may_not_end_with_b(s: re_lang("a+b*")) -> bool:
    return s.endswith("b")


# __contains__
def should_contain_a(s: re_lang("a+b+")) -> Literal[True]:
    return "a" in s


def should_contain_ab(s: re_lang("a+b+")) -> Literal[True]:
    return "ab" in s


# upper, lower
def re_to_upper(s: re_lang("a+b+")) -> re_lang("A+B+"):
    return s.upper()


def re_to_lower(s: re_lang("A+b+")) -> re_lang("a+b+"):
    return s.lower()


# __getitem__
def re_getitem_det(s: re_lang("a+b+")) -> Literal["a"]:
    return s[0]


def re_getitem_nondet(s: re_lang("a+b+")) -> re_lang("a|b"):
    return s[1]


def re_getitem_out_of_bound(s: re_lang("a+b+")) -> str:
    return s[2]  # type error
