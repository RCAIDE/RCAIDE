## @ingroup Library-Methods-Mission-Common-Update
# RCAIDE/Library/Methods/Missions/Common/Update/Aerodynamics.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import numpy as np 
    
# ----------------------------------------------------------------------------------------------------------------------
#  Update Freestream
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Mission-Common-Update
def freestream(segment):
    """ Updates the freestream conditions 
        
        Assumptions:
        N/A
        
        Inputs:
            segment.state.conditions.:
                 frames.inertial.velocity_vector   [m/s]
                 freestream.density                [kg/m^3]
                 freestream.speed_of_sound         [m/s]
                 freestream.dynamic_viscosity      [Pa-s]
        Outputs:
            segment.conditions.freestream
                 velocity                          [m/s]
                 mach_number                       [-]
                 reynolds_number                   [-]
                 dynamic_pressure                  [Pa] 
      
        Properties Used:
        N/A
                    
    """   
    
    # unpack
    conditions = segment.state.conditions
    V          = conditions.frames.inertial.velocity_vector
    rho        = conditions.freestream.density
    a          = conditions.freestream.speed_of_sound
    mu         = conditions.freestream.dynamic_viscosity

    # velocity magnitude
    Vmag2 = np.sum( V**2, axis=1)[:,None]  
    Vmag  = np.sqrt(Vmag2)

    # dynamic pressure
    q = 0.5 * rho * Vmag2 # Pa

    # Mach number
    M = Vmag / a

    # Reynolds number
    Re = rho * Vmag / mu  # per m

    # pack
    conditions.freestream.velocity         = Vmag
    conditions.freestream.mach_number      = M
    conditions.freestream.reynolds_number  = Re
    conditions.freestream.dynamic_pressure = q

    return




def _freestream(State, Settings, System):
	'''
	Framework version of freestream.
	Wraps freestream with State, Settings, System pack/unpack.
	Please see freestream documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = freestream('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System