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


def expects_many_a(s: Re["a*"]) -> str:
    return s


def expects_at_least_one_a(s: Re["a+"]) -> str:
    return s


def expects_a_or_b(s: Re["a|b"]) -> str:
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
