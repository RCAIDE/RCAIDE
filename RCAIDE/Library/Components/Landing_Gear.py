# RCAIDE/Library/Components/Landing_Gear.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: May, 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT 
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import equinox as eqx

# RCAIDE imports  
from RCAIDE.Library import Component

# ----------------------------------------------------------------------------------------------------------------------
# Landing_Gear
# ----------------------------------------------------------------------------------------------------------------------


class LandingGear(Component):

    tag:                str     = eqx.field(static=True, default='Landing Gear')

    deployed:           bool    = False

    number_of_units:    int     = eqx.field(static=True, default=1)
    number_of_wheels:   int     = eqx.field(static=True, default=0)

    strut_length:       float   = 0.
    tire_diameter:      float   = 0.
