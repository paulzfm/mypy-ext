class Refinable:
    """Every class that serves as a type constructor for a refinement type must inherit from this class.
    In this way, during semantic analysis, type variables will not be sought in its arguments
    (since they are expressions)."""


class Refinable1:
    """A Refinable but the first argument is a type parameter."""


class RefinementTypeWrapper:
    """Every user-level function that constructs a refinement type should return an object of this class.
    Based on this wrapper object, the refinement type plugin should build a `mypy.types.RefinementType`.
    This is a trick to avoid the exposure of our internal `mypy.types.RefinementType` to the user.
    """
