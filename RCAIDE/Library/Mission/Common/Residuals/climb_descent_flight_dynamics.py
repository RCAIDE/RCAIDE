## @ingroup Library-Missions-Common-Residuals
# RCAIDE/Library/Missions/Common/Residuals/climb_descent_flight_dynamics.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE

# Python imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Residual Total Forces
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Missions-Common-Residuals
def climb_descent_flight_dynamics(segment):
    """Computes residuals for the force and moment equations of motion of aircraft in varying altitude flight.

        Assumptions:
            None
        
        Args: 
            segment  : flight segment        [-] 
            
        Returns:
            None 
    """        

    if type(segment) == RCAIDE.Framework.Mission.Segments.Transition.Constant_Acceleration_Constant_Angle_Linear_Climb: 
        v       = segment.state.conditions.frames.inertial.velocity_vector
        D       = segment.state.numerics.time.differentiate 
        segment.state.conditions.frames.inertial.acceleration_vector = np.dot(D,v)

    FT = segment.state.conditions.frames.inertial.total_force_vector
    a  = segment.state.conditions.frames.inertial.acceleration_vector    
    
    if type(segment) == RCAIDE.Framework.Mission.Segments.Transition.Constant_Acceleration_Constant_Angle_Linear_Climb: 
        omega = segment.state.conditions.frames.inertial.angular_velocity_vector
        D  = segment.state.numerics.time.differentiate   
        segment.state.conditions.frames.inertial.angular_acceleration_vector =  np.dot(D,omega)         
        
    MT      = segment.state.conditions.frames.inertial.total_moment_vector    
    ang_acc = segment.state.conditions.frames.inertial.angular_acceleration_vector  
    m       = segment.state.conditions.weights.total_mass
    I       = segment.analyses.aerodynamics.geometry.mass_properties.moments_of_inertia.tensor  

    if segment.flight_dynamics.force_x: 
        segment.state.residuals.force_x[:,0] = FT[:,0]/m[:,0] - a[:,0]
    if segment.flight_dynamics.force_y: 
        segment.state.residuals.force_y[:,0] = FT[:,1]/m[:,0] - a[:,1]       
    if segment.flight_dynamics.force_z: 
        segment.state.residuals.force_z[:,0] = FT[:,2]/m[:,0] - a[:,2]
    if  segment.flight_dynamics.moment_x:
        segment.state.residuals.moment_x[:,0] = MT[:,0]/I[0,0] - ang_acc[:,0]   
    if  segment.flight_dynamics.moment_y:
        segment.state.residuals.moment_y[:,0] = MT[:,1]/I[1,1] - ang_acc[:,1]   
    if  segment.flight_dynamics.moment_z:
        segment.state.residuals.moment_z[:,0] = MT[:,2]/I[2,2] - ang_acc[:,2]   
        


    return
