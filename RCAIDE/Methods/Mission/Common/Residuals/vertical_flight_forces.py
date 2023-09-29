## @ingroup Methods-Missions-Common-Residuals
# RCAIDE/Methods/Missions/Common/Residuals/vertical_flight_forces.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Residual Total Forces
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Common-Residuals  
def vertical_flight_forces(segment):
    """ Calculates a residual based on forces
    
        Assumptions:
        The vehicle is not accelerating, doesn't use gravity. Only vertical forces
        
        Inputs:
            state.conditions:
                frames.inertial.total_force_vector [Newtons]
            
        Outputs:
            state.residuals.forces [meters/second^2]

        Properties Used:
        N/A
                                
    """            
    
    FT = segment.state.conditions.frames.inertial.total_force_vector

    # vertical
    segment.state.residuals.forces[:,0] = FT[:,2]

    return
    
    
 
    
