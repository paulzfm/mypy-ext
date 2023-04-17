class RefinementTypeWrapper:
    """Every user-level function that constructs a refinement type should return an object of this class.
    Based on this wrapper object, the refinement type plugin should build a `mypy.types.RefinementType`.
    This is a trick to avoid the exposure of our internal `mypy.types.RefinementType` to the user.
    """
