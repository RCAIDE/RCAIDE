# RCAIDE/Library/Attributes/Solids/Solid.py
# (c) Copyright 2023 Aerospace Research Community LLC 
 
#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

# package imports
import equinox as eqx

#-------------------------------------------------------------------------------
# Solid Data Class
#------------------------------------------------------------------------------- 


class Solid(eqx.Module):

    ultimate_tensile_strength:  float | None = eqx.field(static=True, default=None)
    ultimate_shear_strength:    float | None = eqx.field(static=True, default=None)
    ultimate_bearing_strength:  float | None = eqx.field(static=True, default=None)
    yield_tensile_strength:     float | None = eqx.field(static=True, default=None)
    yield_shear_strength:       float | None = eqx.field(static=True, default=None)
    yield_bearing_strength:     float | None = eqx.field(static=True, default=None)
    minimum_gage_thickness:     float | None = eqx.field(static=True, default=None)
    density:                    float | None = eqx.field(static=True, default=None)

class Aluminum(Solid):
    """
    Physical Constants Specific to 6061-T6 Aluminum

    Source:
            Cao W, Zhao C, Wang Y, et al. Thermal modeling of full-size-scale cylindrical battery pack cooled
            by channeled liquid flow[J]. International journal of heat and mass transfer, 2019, 138: 1178-1187.
    """

    density                    : float | None = eqx.field(static=True, default=2719)
    thermal_conductivity       : float | None = eqx.field(static=True, default=202.4)
    specific_heat_capacity     : float | None = eqx.field(static=True, default=871)