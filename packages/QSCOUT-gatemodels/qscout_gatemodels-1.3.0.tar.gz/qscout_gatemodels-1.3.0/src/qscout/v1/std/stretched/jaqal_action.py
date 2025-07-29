from jaqalpaq.core.stretch import stretched_unitaries

from .. import jaqal_action

IDEAL_ACTION = stretched_unitaries(jaqal_action.IDEAL_ACTION, suffix="_stretched")
