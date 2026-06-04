# RCAIDE/Framework/Analyses/Propulsion/Turbofan_Performance.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: May, 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT 
# ----------------------------------------------------------------------------------------------------------------------

import equinox as eqx

from RCAIDE.Framework import Process, ProcessStep

from RCAIDE.Library.Methods.Energy.Converters.Nozzles import *
from RCAIDE.Library.Methods.Energy.Converters.Turbines import *
from RCAIDE.Library.Methods.Energy.Converters.Turbofans import *
from RCAIDE.Library.Methods.Energy.Converters.Combustors import *
from RCAIDE.Library.Methods.Energy.Converters.Fan_Compressors import *
from RCAIDE.Library.Methods.Energy.Converters.Shaft_Offtake import *


# ----------------------------------------------------------------------------------------------------------------------
# Turbofan_Performance
# ----------------------------------------------------------------------------------------------------------------------

def _build_turbofan_steps() -> tuple[ProcessStep, ...]:
    """Builds the static pipeline of turbofan cycle analysis steps."""
    return (
        ProcessStep(tag="Inlet Nozzle", function=inlet_nozzle_performance),
        ProcessStep(tag="Fan", function=fan_performance),
        ProcessStep(tag="Compressor", function=compressor_performance),
        ProcessStep(tag="Combustor", function=turbojet_combustor_performance),
        ProcessStep(tag="Turbine", function=turbine_performance),
        ProcessStep(tag="Core Nozzle", function=core_nozzle_performance),
        ProcessStep(tag="Fan Nozzle", function=fan_nozzle_performance),
        ProcessStep(tag="Thrust", function=thrust_and_power),
    )

class TurbofanPerformance(Process):
    tag: str = eqx.field(static=True, default='Turbofan Performance')
    
    # Hand the builder function directly to the factory
    steps: tuple[ProcessStep, ...] = eqx.field(default_factory=_build_turbofan_steps)


