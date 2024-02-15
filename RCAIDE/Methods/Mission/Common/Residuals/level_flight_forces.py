## @ingroup Methods-Missions-Common-Residuals
# RCAIDE/Methods/Missions/Common/Residuals/level_flight_forces.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import RCAIDE
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Residual Total Forces
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Common-Residuals
def level_flight_forces(segment):
    """ Calculates a force residuals
    
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
    if 'acceleration' in segment:
        ax      = segment.acceleration  
        one_row = segment.state.ones_row 
        a       = one_row(3)*0
        a[:,0]  = ax 
        segment.state.conditions.frames.inertial.acceleration_vector = a
    elif type(segment) == RCAIDE.Analyses.Mission.Segments.Cruise.Constant_Pitch_Rate_Constant_Altitude:  
        v  = segment.state.conditions.frames.inertial.velocity_vector
        D  = segment.state.numerics.time.differentiate   
        segment.state.conditions.frames.inertial.acceleration_vector =  np.dot(D,v)
        
    FT = segment.state.conditions.frames.inertial.total_force_vector
    a  = segment.state.conditions.frames.inertial.acceleration_vector
    m  = segment.state.conditions.weights.total_mass[:,0]
    
    if segment.flight_dynamics.force_x: 
        segment.state.residuals.force_x[:,0] = FT[:,0]/m[:,0] - a[:,0]
    if segment.flight_dynamics.force_y: 
        segment.state.residuals.force_y[:,0] = FT[:,1]/m[:,0] - a[:,1]       
    if segment.flight_dynamics.force_z: 
        segment.state.residuals.force_z[:,0] = FT[:,2]/m[:,0] - a[:,2]   

    return
    
    
 
    
