# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Motor/size_motor_mass.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Framework.Core import Units

# ----------------------------------------------------------------------------------------------------------------------  
# size_motor_from_mass
# ----------------------------------------------------------------------------------------------------------------------   
def size_motor_from_mass(motor):
    """ Sizes motor from mass based on correlations. The following perperties
        are computed  
        motor.resistance       (float): motor resistance       [ohms]
        motor.no_load_current  (float): motor no-load current  [A] 
        motor.speed_constant   (float): motor speed constant   [RPM/V]
    
    Source:
        Gur, O., Rosen, A, AIAA 2008-5916.
    
    Args:
        motor.mass       (float): motor mass   [kg]
    
    Returns:
    None 

    """
    # unpack 
    mass = motor.mass_properties.mass  
    
    B_KV = 50.   * Units['rpm*kg/volt']
    B_RA = 60000.* Units['(rpm**2)*ohm/(V**2)']
    B_i0 = 0.2   * Units['amp*(ohm**0.6)']
    
    # compute properties 
    KV   = B_KV/mass
    res  = B_RA/(KV**2.)
    i0   = B_i0/(res**0.6) 

    # store motor properties 
    motor.speed_constant  = KV   
    motor.resistance      = res 
    motor.no_load_current = i0   

    return  