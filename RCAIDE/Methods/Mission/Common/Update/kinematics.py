## @ingroup Methods-Missions-Common Common-Update
# RCAIDE/Methods/Missions/Common/Update/kinematics.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Acceleration
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Segments-Common-Update
def kinematics(segment):
    """  
                                
    """            
    
    # unpack conditions
    v = segment.state.conditions.frames.inertial.velocity_vector
    D = segment.state.numerics.time.differentiate
    
    # accelerations
    acc = np.dot(D,v)
    
    # pack conditions
    segment.state.conditions.frames.inertial.acceleration_vector[:,:] = acc[:,:]   