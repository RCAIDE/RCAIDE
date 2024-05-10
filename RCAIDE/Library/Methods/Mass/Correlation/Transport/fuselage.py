# RCAIDE/Library/Methods/Mass/Correlation/Transport/fuselage.py
# (c) Copyright 2024 Aerospace Research Community LLC
# Created:  May 2024, J. Smart
# Modified: 
#-------------------------------------------------------------------------------
#  Imports
#-------------------------------------------------------------------------------

from RCAIDE.Framework.Core import Units
from RCAIDE.Library.Components import Fuselage

import numpy as np

#-------------------------------------------------------------------------------
#  Functional/Library Version
#-------------------------------------------------------------------------------

def func_fuselage(
        fuselage_wetted_area: np.ndarray,
        fuselage_width: np.ndarray,
        fuselage_maximum_height: np.ndarray,
        fuselage_total_length: np.ndarray,
        fuselage_differential_pressure: np.ndarray,
        vehicle_limit_load: np.ndarray,
        vehicle_max_zero_fuel_mass: np.ndarray,
        vehicle_main_wing_mass: np.ndarray,
        vehicle_main_wing_root_chord: np.ndarray,
        vehicle_propulsion_mass: np.ndarray
                 ):
    """
    Library version of fuselage.
    
    Parameters
    ----------
    fuselage_wetted_area : np.ndarray
        Fuselage wetted area in square meters

    fuselage_width : np.ndarray
        Fuselage width in meters

    fuselage_maximum_height : np.ndarray
        Fuselage maximum height in meters

    fuselage_total_length : np.ndarray
        Fuselage total length in meters

    fuselage_differential_pressure : np.ndarray
        Fuselage differential pressure in Pascals

    vehicle_limit_load : np.ndarray
        Zero fuel weight limit load factor

    vehicle_max_zero_fuel_mass : np.ndarray
        Maximum vehicle zero fuel mass in kilograms

    vehicle_main_wing_mass : np.ndarray
        Vehicle main wing mass in kilograms

    vehicle_main_wing_root_chord : np.ndarray
        Vehicle main wing root chord in meters

    vehicle_propulsion_mass : np.ndarray
        Vehicle propulsion system mass in kilograms

    Returns
    -------
    fuselage_mass : np.ndarray
        Fuselage mass in kilograms
       
    See Also
    --------
    N/A
    
    Notes
    -----
    Correlation of fuselage mass with differential pressure or limit load as appropriate.
    
    References
    ----------
    
    Examples
    --------
    func_fuselage(*args):
        82000.0
    
    """
    
    # Unit Conversion

    dp  = fuselage_differential_pressure / (Units.lbf / Units.ft ** 2)
    w   = fuselage_width / Units.ft
    h   = fuselage_maximum_height / Units.ft
    l   = (fuselage_total_length - vehicle_main_wing_root_chord/2.) / Units.ft
    m   = (vehicle_max_zero_fuel_mass - vehicle_main_wing_mass - vehicle_propulsion_mass) / Units.lbm
    S   = fuselage_wetted_area / Units.ft ** 2

    # Limiting Factor Determination

    pressure_idx = 1.50E-3 * dp * w
    geometry_idx = 1.91E-4 * vehicle_limit_load * m * l/h**2

    if pressure_idx > geometry_idx:
        limit_idx = pressure_idx
    else:
        limit_idx = (pressure_idx**2 + geometry_idx**2)/(2*geometry_idx)

    fuselage_mass = ((1.051 + 0.102 * limit_idx) * S) * Units.lbm
    
    return fuselage_mass

#-------------------------------------------------------------------------------
#  Stateful/Framework Version
#-------------------------------------------------------------------------------

def fuselage(State, Settings, System):
    """
    Framework version of fuselage
    
    See Also
    --------
    func_fuselage: 
        Functional implementation which this method calls.
    """

    fuselage_wetted_area            = np.atleast_1d([f.areas.wetted for f in System.fuselages])
    fuselage_width                  = np.atleast_1d([f.widths.maximum for f in System.fuselages])
    fuselage_maximum_height         = np.atleast_1d([f.heights.maximum for f in System.fuselages])
    fuselage_total_length           = np.atleast_1d([f.lengths.total for f in System.fuselages])
    fuselage_differential_pressure  = np.atleast_1d([f.differential_pressure for f in System.fuselages])
    vehicle_limit_load              = np.atleast_1d(System.envelope.limit_load)
    vehicle_max_zero_fuel_mass      = np.atleast_1d(System.mass_properties.max_zero_fuel_mass)
    vehicle_main_wing_mass          = np.atleast_1d(System.wings.main_wing.mass_properties.mass)
    vehicle_main_wing_root_chord    = np.atleast_1d(System.wings.main_wing.chords.root)
    vehicle_propulsion_mass         = np.atleast_1d(System.energy_network.converters.propulsors.mass_properties.mass)

    results = func_fuselage(fuselage_wetted_area,
                            fuselage_width,
                            fuselage_maximum_height,
                            fuselage_total_length,
                            fuselage_differential_pressure,
                            vehicle_limit_load,
                            vehicle_max_zero_fuel_mass,
                            vehicle_main_wing_mass,
                            vehicle_main_wing_root_chord,
                            vehicle_propulsion_mass)
                           
    for idx, fuse in enumerate(System.fuselages):
        fuse.mass_properties.mass = results[idx]

    System.sum_mass()
    
    return State, Settings, System
                           
    
