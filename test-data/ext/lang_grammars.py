from fuzzingbook.Grammars import Grammar

from mypy_ext.lang_type import lang

DIGIT_GRAMMAR: Grammar = {
    "<start>": ["<digit>"],
    "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

Digit = lang(DIGIT_GRAMMAR, 'DIGIT')
