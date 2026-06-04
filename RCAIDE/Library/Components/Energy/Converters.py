# RCAIDE/Library/Components/Energy/Converter.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: Apr 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import equinox as eqx

# RCAIDE imports
from RCAIDE.Library import Component

# ----------------------------------------------------------------------------------------------------------------------
#  Energy Converter
# ----------------------------------------------------------------------------------------------------------------------


class EnergyConverter(Component):

    efficiency:                 float = 1.0

# ----------------------------------------------------------------------------------------------------------------------
# Propulsor Subcomponents
# ----------------------------------------------------------------------------------------------------------------------

class FlowConverter(EnergyConverter):

    mechanical_efficiency:      float = 1.0
    polytropic_efficiency:      float = 1.0

    pressure_ratio:             float = 1.0
    pressure_recovery:          float = 1.0
    area_ratio:                 float = 1.0

    design_intake_temperature:  float = 298.15    # Kelvin

    rotation_speed:             float = 0.0
    noise_speed:                float = 0.0


class OfftakeShaft(EnergyConverter):

    tag: str = eqx.field(static=True, default="Offtake Shaft")

    power_draw:             float = 0.0
    reference_temperature:  float = 298.15      # Kelvin
    reference_pressure:     float = 101325.0    # Pascal

