from mypy.typing_extension import RefinementTypeWrapper


class FiniteTypeWrapper(RefinementTypeWrapper):
    bound: int

    def __init__(self, bound: int):
        self.bound = bound


def fin(bound: int) -> FiniteTypeWrapper:
    return FiniteTypeWrapper(bound)
