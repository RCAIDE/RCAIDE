# RCAIDE/Library/Missions/Common/Update/atmosphere.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  Update Atmosphere
# ----------------------------------------------------------------------------------------------------------------------
def atmosphere(segment):
    """ Computes conditions of the atmosphere at given altitudes
    
        Assumptions:
        None
        
        Args:
            state.conditions:
                freestream.altitude             [meters]
            segment.analyses.atmoshere          [Function]
            
        Returns:
            state.conditions:
                freestream.pressure             [pascals]
                freestream.temperature          [kelvin]
                freestream.density              [kilogram/meter^3]
                freestream.speed_of_sound       [meter/second]
                freestream.dynamic_viscosity    [pascals-seconds]
                freestream.kinematic_viscosity  [meters^2/second]
                freestream.thermal_conductivity [Watt/meter-Kelvin]
                freestream.prandtl_number       [unitless] 
    """
    
    # unpack
    conditions            = segment.state.conditions
    h                     = conditions.freestream.altitude
    temperature_deviation = segment.temperature_deviation
    atmosphere            = segment.analyses.atmosphere
    
    # compute
    atmosphere_data = atmosphere.compute_values(h,temperature_deviation)
    
    # pack
    conditions.freestream.pressure               = atmosphere_data.pressure
    conditions.freestream.temperature            = atmosphere_data.temperature
    conditions.freestream.thermal_conductivity   = atmosphere_data.thermal_conductivity
    conditions.freestream.density                = atmosphere_data.density
    conditions.freestream.speed_of_sound         = atmosphere_data.speed_of_sound
    conditions.freestream.dynamic_viscosity      = atmosphere_data.dynamic_viscosity
    conditions.freestream.kinematic_viscosity    = atmosphere_data.kinematic_viscosity
    conditions.freestream.prandtl_number         = atmosphere_data.prandtl_number
    
    return
     