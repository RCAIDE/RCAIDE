## @ingroup Methods-Missions-Common-Update 
# RCAIDE/Methods/Missions/Common/Update/weights.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Update Weights
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Common-Update  
def weights(segment): 
    """  
                                
    """          
    
    # unpack
    conditions   = segment.state.conditions
    I            = segment.state.numerics.time.integrate  
    m0           = conditions.weights.total_mass[0,0]
    mdot_fuel    = conditions.weights.vehicle_mass_rate
    g            = conditions.freestream.gravity 

    # calculate
    m = m0 + np.dot(I, -mdot_fuel )

    # weight
    W = m*g

    # pack
    conditions.weights.total_mass[1:,0]                  = m[1:,0]  
    conditions.frames.inertial.gravity_force_vector[:,2] = W[:,0]

    return
 