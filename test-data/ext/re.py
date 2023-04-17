from typing import Literal

from re_types import *


def re_cast() -> None:
    s1: re_lang("ab") = "ab"
    s2: str = s1
    s3: Literal["hello"] = "hello"
    s4: re_lang("hello") = s3
    n: int = len(s4)


def re_subtype(s: re_lang("a+")) -> re_lang("a*"):
    return s


def expects_many_a(s: many_a) -> str:
    return s


def expects_at_least_one_a(s: at_least_one_a) -> str:
    return s


def expects_a_or_b(s: a_or_b) -> str:
    return s


def test() -> None:
    expects_many_a("")
    expects_many_a("a")
    expects_many_a("aa")

    # expects_at_least_one_a("")  # type error
    expects_at_least_one_a("a")
    expects_at_least_one_a("aa")

    expects_a_or_b("a")
    expects_a_or_b("b")
    # expects_a_or_b("c")  # type error
