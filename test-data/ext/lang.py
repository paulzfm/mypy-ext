from fuzzingbook.Grammars import US_PHONE_GRAMMAR
from lang_grammars import *


def expect_us_phone_number(s: lang(US_PHONE_GRAMMAR, 'US_PHONE')) -> str:
    return s


def test_us_phone_number() -> None:
    expect_us_phone_number("(692)449-5179")
    expect_us_phone_number("(692)449-517")  # type error


def expect_digit(s: Digit) -> str:
    return s


def test_digit() -> None:
    expect_digit('0')
    expect_digit('5')
    expect_digit('9')
    expect_digit('123')  # type error
    expect_digit('A')  # type error
