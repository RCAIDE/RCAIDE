# RCAIDE/Methods/Missions/Segments/Cruise/Common.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# Pacakge imports 
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Segments-Cruise
def unpack_unknowns(segment):
    """ Unpacks the throttle setting and body angle from the solver to the mission
    
        Assumptions:
        N/A
        
        Inputs:
            state.unknowns:
                throttle    [Unitless]
                body_angle  [Radians]
            
        Outputs:
            state.conditions:
                propulsion.throttle            [Unitless]
                frames.body.inertial_rotations [Radians]

        Properties Used:
        N/A
                                
    """    
     
    if 'thottle' in segment.state.unknowns: 
        throttle = segment.state.unknowns.throttle
        segment.state.conditions.energy.throttle[:,0] = throttle[:,0]
         
    body_angle = segment.state.unknowns.body_angle 
    segment.state.conditions.frames.body.inertial_rotations[:,1] = body_angle[:,0]   
    

# ----------------------------------------------------------------------
#  Residual Total Forces
# ----------------------------------------------------------------------

## @ingroup Methods-Missions-Segments-Cruise
def residual_total_forces(segment):
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
    
    
 
    
    