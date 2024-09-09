# B737 Analysis List
#
# 1. Sizing         (Doesn't Do Anything)
# 2. Weights
# 3. Aerodynamics   (Fidelity Zero)
# 4. Stability      (Fidelity Zero)
# 5. Energy
# 6. Planet
# 7. Atmosphere

# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass

# package imports

import numpy as np
from pint import UnitRegistry
units = UnitRegistry()

# RCAIDE imports

import RCAIDE.Framework as rcf

from RCAIDE.Library.Attributes.AC_Classes import MediumRange


# ----------------------------------------------------------------------------------------------------------------------
# Vehicle Setup
# ----------------------------------------------------------------------------------------------------------------------

def vehicle_setup():

    B737 = rcf.System(name='Boeing 737')

    # System-Level Properties

    B737.aircraft_type      = MediumRange()
    B737.areas.reference    = 124.862 * units.m ** 2
    B737.passengers         = 170

    # Mass Properties

    B737.mass_properties.max_takeoff        = 79015.8 * units.kilogram
    B737.mass_properties.takeoff            = 79015.8 * units.kilogram

    B737.mass_properties.operating_empty    = 62746.4 * units.kilogram
    B737.mass_properties.max_zero_fuel      = 62732.0 * units.kilogram
    B737.mass_properties.cargo              = 10000.0 * units.kilogram

    B737.mass_properties.center_of_gravity  = np.array([13.72, 0, -1.0])

    # --- Landing Gear ---

    LG = rcf.Component(name='Landing Gear')

    LG.num_main_units       = 2
    LG.num_main_wheels      = 2
    LG.main_strut_length    = 1.8 * units.m
    LG.main_tire_diameter   = 1.12 * units.m

    LG.num_nose_units       = 1
    LG.num_nose_wheels      = 2
    LG.nose_strut_length    = 1.3 * units.m
    LG.nose_tire_diameter   = 0.6858 * units.m

    B737.add_subcomponent(LG)

    # --- Main Wing ---

    MW = rcf.Components.Wing(name='Main Wing')

    MW.vertical = False
    MW.symmetric = True
    MW.high_lift = True

    MW.aspect_ratio = 10.18
    MW.thickness_to_chord = 0.1
    MW.taper = 0.1

    MW.spans.projected = 34.32

    MW.sweeps.quarter_chord = 25 * units.deg

    MW.chords.root = 7.760 * units.meter
    MW.chords.tip = 0.782 * units.meter
    MW.chords.mean_aerodynamic = 4.235 * units.meter

    MW.areas.reference = 124.862
    MW.areas.wetted = 225.08

    MW.twists.root = 4.0 * units.degrees
    MW.twists.tip = 0.0 * units.degrees

    MW.origin = np.array([13.61, 0, -0.5])
    MW.aerodynamic_center = np.array([0, 0, 0])

    # --- --- Root Segment --- ---

    # --- --- Yehudi Segment --- ---

    # --- --- Mid Segment --- ---
    
    # --- --- Tip Segment --- ---

    # --- --- Control Surfaces --- ---

    # --- --- --- Slat --- --- ---

    # --- --- --- Flap --- --- ---

    # --- --- --- Aileron --- --- ---

    B737.add_subcomponent(MW)










