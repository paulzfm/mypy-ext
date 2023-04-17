from mypy_ext.regular_type import re_lang

at_least_one_a = re_lang("a+")
many_a = re_lang("a*")
a_or_b = re_lang("a|b")
