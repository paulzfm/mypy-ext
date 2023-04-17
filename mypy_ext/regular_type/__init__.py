from mypy.typing_extension import RefinementTypeWrapper


class RegularTypeWrapper(RefinementTypeWrapper):
    regex: str

    def __init__(self, regex: str):
        self.regex = regex


def re_lang(regex: str) -> RegularTypeWrapper:
    return RegularTypeWrapper(regex)
