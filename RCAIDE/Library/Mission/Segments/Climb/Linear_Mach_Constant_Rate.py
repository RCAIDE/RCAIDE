## @ingroup Library-Missions-Segments-Climb
# RCAIDE/Library/Missions/Segments/Climb/Linear_Mach_Constant_Rate.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE 
from RCAIDE.Library.Mission.Common.Update.atmosphere import atmosphere

# Package imports  
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Missions-Segments-Climb
def initialize_conditions(segment):
    
    """Sets the specified conditions which are given for the segment type.
    
    Assumptions:
    Linearly changing mach number, with a constant rate of climb

    Source:
    N/A

    Inputs:
    segment.climb_rate                                  [meters/second]
    segment.mach_number_start                                  [Unitless]
    segment.mach_number_end                                    [Unitless]
    segment.altitude_end                                [meters]
    segment.state.numerics.dimensionless.control_points [Unitless]
    conditions.freestream.density                       [kilograms/meter^3]

    Outputs:
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]

    Properties Used:
    N/A
    """          
    
    # unpack
    climb_rate = segment.climb_rate
    M0         = segment.mach_number_start
    Mf         = segment.mach_number_end
    alt0       = segment.altitude_start 
    altf       = segment.altitude_end 
    beta       = segment.sideslip_angle
    t_nondim   = segment.state.numerics.dimensionless.control_points
    conditions = segment.state.conditions
    
    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2]

    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0
    conditions.freestream.altitude[:,0]             =  alt[:,0] # positive altitude in this context
    

    # Update freestream to get speed of sound
    atmosphere(segment)
    a          = conditions.freestream.speed_of_sound
    
    # check for initial velocity
    if M0 is None: 
        if not segment.state.initials: raise AttributeError('airspeed not set')
        M0 = np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1])/ a
         
    # process velocity vector
    mach_number = (Mf-M0)*t_nondim + M0
    v_mag       = mach_number * a
    v_z         = -climb_rate # z points down
    v_xy        = np.sqrt( v_mag**2 - v_z**2 )
    v_x         = np.cos(beta)*v_xy
    v_y         = np.sin(beta)*v_xy
    
    # pack conditions    
    conditions.frames.inertial.velocity_vector[:,0] = v_x[:,0]
    conditions.frames.inertial.velocity_vector[:,1] = v_y[:,0]
    conditions.frames.inertial.velocity_vector[:,2] = v_z
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0] # z points down
    conditions.freestream.altitude[:,0]             =  alt[:,0] # positive altitude in this context
    