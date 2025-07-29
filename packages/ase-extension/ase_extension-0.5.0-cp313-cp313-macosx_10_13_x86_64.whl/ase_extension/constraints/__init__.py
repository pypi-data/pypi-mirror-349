from ase import constraints

from .bias import RMSDBiasPotential
from .confine import ConfineSphere
from .fix import FixBondLengths

__all__ = [
    "ConfineSphere",
    "FixBondLengths",
    "RMSDBiasPotential",
]


def dict2constraint(dct):
    name = dct["name"]
    kwargs = dct["kwargs"]
    # First search in the current module (it takes precedence)
    if name in __all__:
        return globals()[name](**kwargs)
    # Then search in the ase.constraints module
    if name in constraints.__all__:
        return getattr(constraints, name)(**kwargs)
    raise ValueError(f"Unknown constraint name: {name}. Available: {__all__ + constraints.__all__}")


# Fix for trajectory IO
constraints.dict2constraint = dict2constraint
