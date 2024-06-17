## @ingroup Library-Missions-Common-Unknowns
# RCAIDE/Library/Missions/Common/Unknowns/ground.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Missions-Common-Unknowns
def ground(segment):
    """Assigns the unknowns for the aircraft velocity to the aircraft each iteration of
       the mission solving process. Computes the following variables:
          segment.state.conditions.frames.inertial.velocity_vector [meters/second]
          segment.state.conditions.frames.inertial.time            [second]

        Assumptions:
            None
        
        Args: 
            segment.state.unknowns.ground_velocity    [meters/second]
            segment.state.unknowns.elapsed_time       [second]
            
        Returns:
            None 
    """          
    
    # unpack unknowns 
    ground_velocity = segment.state.unknowns.ground_velocity
    time            = segment.state.unknowns.elapsed_time
    
    # unpack givens
    v0         = segment.air_speed_start  
    t_initial  = segment.state.conditions.frames.inertial.time[0,0]
    t_nondim   = segment.state.numerics.dimensionless.control_points
    
    # time
    t_final    = t_initial + time  
    times      = t_nondim * (t_final-t_initial) + t_initial     

    # apply unknowns
    conditions = segment.state.conditions
    conditions.frames.inertial.velocity_vector[1:,0] = ground_velocity
    conditions.frames.inertial.velocity_vector[0,0]  = v0
    conditions.frames.inertial.time[:,0]             = times[:,0]
    
    return 