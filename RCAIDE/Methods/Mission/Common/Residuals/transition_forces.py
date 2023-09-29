## @ingroup Methods-Missions-Common-Residuals
# RCAIDE/Methods/Missions/Common/Residuals/transition_forces.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
  
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# Pacakge imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Residual Total Forces
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Common-Residuals 
def transition_forces(segment):
    """ Calculates a residual based on forces
    
        Assumptions:
        The vehicle is not accelerating, doesn't use gravity
        
        Inputs:
            segment.state.conditions:
                frames.inertial.total_force_vector [Newtons]
                weights.total_mass                 [kg]
            
        Outputs:
            segment.state.residuals.forces [meters/second^2]

        Properties Used:
        N/A
                                
    """        
    
    FT = segment.state.conditions.frames.inertial.total_force_vector
    m  = segment.state.conditions.weights.total_mass[:,0] 
    
    # horizontal
    segment.state.residuals.forces[:,0] = np.sqrt( FT[:,0]**2. + FT[:,1]**2. )/m
    # vertical
    segment.state.residuals.forces[:,1] = FT[:,2]/m

    return
    
    
 
    
    