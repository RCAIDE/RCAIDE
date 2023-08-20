# RCAIDE/Methods/Missions/Segments/Hover/Common.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 
 
# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Methods-Missions-Segments-Hover
def unpack_unknowns(segment):
    """ Unpacks the throttle setting from the solver to the mission
    
        Assumptions:
        N/A
        
        Inputs:
            state.unknowns:
                throttle    [Unitless]
            
        Outputs:
            state.conditions:
                propulsion.throttle            [Unitless]

        Properties Used:
        N/A
                                
    """     
    

    if 'thottle' in segment.state.unknowns: 
        throttle = segment.state.unknowns.throttle
        segment.state.conditions.energy.throttle[:,0] = throttle[:,0] 
    
# ----------------------------------------------------------------------------------------------------------------------  
#  Residual Total Forces
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Methods-Missions-Segments-Hover
def residual_total_forces(segment):
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
    segment.state.residuals.force[:,0] = FT[:,2]

    return
    
    
 
    
    