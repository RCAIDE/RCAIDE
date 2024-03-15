## @ingroup Methods-Energy-Propulsors-Converters-Motor
# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Motor/size_motor_from_Kv.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Framework.Core import Units

# ----------------------------------------------------------------------------------------------------------------------  
#  size_from_kv
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Energy-Propulsors-Converters-Motor
def size_motor_from_Kv(motor):
    """
    Determines a motors mass based on the speed constant KV
    
    Source:
    Gur, O., Rosen, A, AIAA 2008-5916.
    
    Inputs:
    motor    (to be modified)
      kv       motor speed constant
    
    Outputs:
    motor.
      resistance         [ohms]
      no_load_current    [amps]
      mass               [kg]
    
    
    """
    
    # Set the KV     
    kv = motor.speed_constant 
    
    # Correlations from Gur:
    # Gur, O., Rosen, A, AIAA 2008-5916. 
    
    B_KV = 50.   * Units['rpm*kg/volt']
    B_RA = 60000.* Units['(rpm**2)*ohm/(volt**2)']
    B_i0 = 0.2   * Units['amp*(ohm**0.6)']
    
    # Do the calculations from the regressions
    mass = B_KV/kv
    res  = B_RA/(kv**2.)
    i0   = B_i0/(res**0.6)
    
    # pack
    motor.resistance           = res
    motor.no_load_current      = i0
    motor.mass_properties.mass = mass
    
    return motor


def _size_motor_from_Kv(State, Settings, System):
	'''
	Framework version of size_motor_from_Kv.
	Wraps size_motor_from_Kv with State, Settings, System pack/unpack.
	Please see size_motor_from_Kv documentation for more details.
	'''

	#TODO: motor = [Replace With State, Settings, or System Attribute]

	results = size_motor_from_Kv('motor',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System