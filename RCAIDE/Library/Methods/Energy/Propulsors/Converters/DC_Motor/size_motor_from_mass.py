## @ingroup Methods-Energy-Propulsors-Converters-Motor
# RCAIDE/Methods/Energy/Propulsors/Converters/Motor/size_motor_mass.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Core import Units 

## @ingroup Methods-Energy-Propulsors-Converters-Motor
def size_motor_from_mass(motor):
    """
    Sizes motor from mass
    
    Source:
    Gur, O., Rosen, A, AIAA 2008-5916.
    
    Inputs:
    motor.    (to be modified)
      mass               [kg]
    
    Outputs:
    motor.
      resistance         [ohms]
      no_load_current    [amps] 
    """     
    mass = motor.mass_properties.mass 
    
    # Correlations from Gur:
    # Gur, O., Rosen, A, AIAA 2008-5916.  
    
    B_KV = 50.   * Units['rpm*kg/volt']
    B_RA = 60000.* Units['(rpm**2)*ohm/(V**2)']
    B_i0 = 0.2   * Units['amp*(ohm**0.6)']
    
    # Do the calculations from the regressions
    kv   = B_KV/mass
    res  = B_RA/(kv**2.)
    i0   = B_i0/(res**0.6) 

    # Unpack the motor
    motor.resistance      = res 
    motor.no_load_current = i0  
    motor.speed_constant  = kv    

    return motor 