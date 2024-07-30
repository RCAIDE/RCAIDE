# RCAIDE/Library/Attributes/Solids/Aluminum.py
# (c) Copyright 2023 Aerospace Research Community LLC
 

# Created: Mar, 2024 M. Clarke
# Modified: May 2024, J. Smart

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from dataclasses import dataclass, field
from RCAIDE.Framework.Core import Units

#-------------------------------------------------------------------------------
# Aluminum for WavyChannel for battery cooling
#-------------------------------------------------------------------------------

@dataclass
class Aluminum:
    """
    Physical Constants Specific to 6061-T6 Aluminum

    Cao W, Zhao C, Wang Y, et al.
    'Thermal modeling of full-size-scale cylindrical battery pack cooled by
    channeled liquid flow.'
    International journal of heat and mass transfer, 2019, 138: 1178-1187.
    """

    material_name               : str = '6061-T6 Aluminum'

    ultimate_tensile_strength   : float = 310e6 * Units.Pa
    ultimate_shear_strength     : float = 206e6 * Units.Pa
    ultimate_bearing_strength   : float = 607e6 * Units.Pa

    yield_tensile_strength      : float = 276e6 * Units.Pa
    yield_shear_strength        : float = 206e6 * Units.Pa
    yield_bearing_strength      : float = 386e6 * Units.Pa

    minimum_gage_thickness      : float = 0.0   * Units.m

    density                     : float = 2719. * Units['kg/(m**3)']
    thermal_conductivity        : float = 202.4 * Units['W/(m*K)']
    specific_heat_capacity      : float = 871   * Units['J/(kg*K)']
