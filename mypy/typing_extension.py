class Refinable:
    """Every class that serves as a type constructor for a refinement type must inherit from this class.
    In this way, during semantic analysis, type variables will not be sought in its arguments
    (since they are expressions)."""
