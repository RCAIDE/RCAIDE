# RCAIDE/Framework/Analyses/Aerodynamics/Test_Aero.py
# (c) Copyright 2026 Aerospace Research Community LLC
#
# Created: Jan, 2026, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT 
# ----------------------------------------------------------------------------------------------------------------------

import equinox as eqx

from RCAIDE.Framework import Process, ProcessStep
from RCAIDE.Framework.Methods.Aerodynamics.Test_Aero import direct_aero


# 1. Define the builder function outside the class
def _build_test_aero_steps():
    """Builds and returns the default tuple of process steps."""
    return (
        ProcessStep(
            tag="Direct Aero Calculation",
            function=direct_aero 
        ),
    )


class TestAero(Process):
    tag: str = eqx.field(static=True, default="Aerodynamics")
    steps: tuple = eqx.field(default_factory=_build_test_aero_steps)