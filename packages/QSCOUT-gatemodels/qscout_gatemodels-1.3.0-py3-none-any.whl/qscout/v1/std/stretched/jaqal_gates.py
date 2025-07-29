# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.
from .. import jaqal_gates, stretched
from jaqalpaq.core.stretch import stretched_gates

# Backwards-compatible import of jaqal_action
__bc_names = set(["abs", "diag", "pi", "kron", "pygsti", "jaqal_gates"])


def __getattr__(name):
    if name not in __bc_names:
        raise AttributeError(f"module '{name}' has no attribute '{name}'")

    import warnings

    warnings.warn("name now in .jaqal_action", DeprecationWarning)
    from . import jaqal_action

    return getattr(jaqal_action, name)


ALL_GATES = jaqal_gates.ALL_GATES.copy()
del ALL_GATES["prepare_all"]
del ALL_GATES["measure_all"]
ALL_GATES = stretched_gates(ALL_GATES, suffix="_stretched", origin=stretched.__name__)
