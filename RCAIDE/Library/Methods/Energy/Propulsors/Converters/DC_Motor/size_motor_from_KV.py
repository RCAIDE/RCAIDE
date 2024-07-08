# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Motor/size_motor_from_Kv.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Framework.Core import Units

# ----------------------------------------------------------------------------------------------------------------------  
#  size_from_kv
# ----------------------------------------------------------------------------------------------------------------------  
def size_motor_from_KV(motor):
    """ Determines a motors mass based on the speed constant, KV. The following perperties
        are computed   
       motor.resistance      (float): motor resistance      [ohms]
       motor.no_load_current (float): motor no-load current [A]
       motor.mass            (float): motor mass            [kg]
    
    Source:
        Gur, O., Rosen, A, AIAA 2008-5916.
    
    Args:
        motor.KV   (float): motor speed constant [RPM/V]
    
    Returns:
        None 
    """
    
    # unpack 
    KV = motor.speed_constant  
    
    B_KV = 50.   * Units['rpm*kg/volt']
    B_RA = 60000.* Units['(rpm**2)*ohm/(volt**2)']
    B_i0 = 0.2   * Units['amp*(ohm**0.6)']
    
    # compute properties 
    mass = B_KV/KV
    res  = B_RA/(KV**2.)
    i0   = B_i0/(res**0.6)
    
    # pack motor properties 
    motor.no_load_current      = i0
    motor.mass_properties.mass = mass
    motor.resistance           = res
    
    return  