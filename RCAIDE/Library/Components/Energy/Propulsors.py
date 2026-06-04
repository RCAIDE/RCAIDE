# RCAIDE/Library/Components/Energy/Propulsors.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: May 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import dataclasses as dc

# package imports
import equinox as eqx

# RCAIDE imports
from RCAIDE.Library import Component
from RCAIDE.Library.Propellants import Propellant, JetA
from RCAIDE.Library.Gases import Gas, Air
from RCAIDE.Library.Components.Energy.Converters import EnergyConverter, FlowConverter, OfftakeShaft

# ----------------------------------------------------------------------------------------------------------------------
# Propulsors
# ----------------------------------------------------------------------------------------------------------------------


class DesignParameters(eqx.Module):

    total_thrust:           float = 0.0

    altitude:               float = 0.0
    mach_number:            float = 0.0
    isa_deviation:          float = 0.0

    SLS_thrust:             float = 0.0

    mass_flow_through_rate: float = 0.0
    fuel_air_ratio:         float = 0.0


class Propulsor(EnergyConverter):

    converters:                 Component           = eqx.field(default_factory=lambda: Component(tag='Propulsor Converters'))

    design_thrust_parameters:   DesignParameters    = eqx.field(default_factory=DesignParameters)

    def compute_thrust(self):
        raise NotImplementedError("Subclasses must implement this method")


# ----------------------------------------------------------------------------------------------------------------------
# Jet Engines
# ----------------------------------------------------------------------------------------------------------------------

class JetInstallationGeometry(eqx.Module):

    xe: float = 1.
    ye: float = 1.
    Ce: float = 2.

def _JetConverters():
    return Component(tag="Jet Converters").add_subcomponent(FlowConverter(tag="Combustor"))

class JetEngine(Propulsor):

    tag:                            str     = eqx.field(static=True, default='Jet')
    plug_diameter:                  float   = 0.0

    reference_temperature:          float   = 288.15      # Kelvin
    reference_total_temperature:    float   = 298.15      # Kelvin

    reference_pressure:             float   = 101325.0    # Pascal
    reference_total_pressure:       float   = 101325.0    # Pascal

    fuel:                   Propellant      = eqx.field(default_factory=JetA)
    working_fluid:          Gas             = eqx.field(default_factory=Air)

    converters:             Component       = eqx.field(default_factory=_JetConverters)

    installation_geometry:  JetInstallationGeometry     = eqx.field(default_factory=JetInstallationGeometry)

def _TurbojetConverters():
    convs = Component(tag="Turbojet Converters")
    convs = convs.add_subcomponent(FlowConverter(tag="Inlet Nozzle"))
    
    comps = Component(tag='Compressors')
    comps = comps.add_subcomponent(FlowConverter(tag='Low Pressure Compressor'))
    comps = comps.add_subcomponent(FlowConverter(tag='High Pressure Compressor'))
    convs = convs.add_subcomponent(comps)

    convs = convs.add_subcomponent(FlowConverter(tag="Combustor"))
    
    turbs = Component(tag='Turbines')
    turbs = turbs.add_subcomponent(FlowConverter(tag='High Pressure Turbine'))
    turbs = turbs.add_subcomponent(FlowConverter(tag='Low Pressure Turbine'))
    convs = convs.add_subcomponent(turbs)

    convs = convs.add_subcomponent(OfftakeShaft())
    convs = convs.add_subcomponent(FlowConverter(tag='Core Nozzle'))

    return convs

class TurbojetEngine(JetEngine):

    tag: str = eqx.field(static=True, default='Turbojet')

    converters: Component = eqx.field(default_factory=_TurbojetConverters)

def _TurbofanConverters():
    convs = _TurbojetConverters()
    convs = dc.replace(convs, tag="Turbofan Converters")
    convs = convs.insert_subcomponent(FlowConverter(tag="Fan"), 0)
    convs = convs.insert_subcomponent(FlowConverter(tag="Fan Nozzle"), 0)

    return convs

class TurbofanEngine(TurbojetEngine):

    tag: str = eqx.field(static=True, default='Turbofan')

    bypass_ratio: float = 1.0
    exa: float = 1.0        # Fan Face-to-Exit Distance

    converters: Component = eqx.field(default_factory=_TurbofanConverters)
