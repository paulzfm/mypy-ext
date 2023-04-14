from mypy_ext.regular_type.typing import re_lang


def re_subtype(s: re_lang("a+")) -> re_lang("a*"):
    return s
