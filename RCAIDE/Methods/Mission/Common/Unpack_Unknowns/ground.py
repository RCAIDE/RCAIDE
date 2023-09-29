## @ingroup Methods-Missions-Common-Unknowns
# RCAIDE/Methods/Missions/Common/Unknowns/ground.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Common-Unknowns
def ground(segment):
    """ Unpacks the times and velocities from the solver to the mission
    
        Assumptions:
        Overrides the velocities if they go to zero
        
        Inputs:
            segment.state.unknowns:
                velocity_x         [meters/second]
                time               [second]
            segment.velocity_start [meters/second]
            
        Outputs:
            segment.state.conditions:
                frames.inertial.velocity_vector [meters/second]
                frames.inertial.time            [second]
        Properties Used:
        N/A
                                
    """       
    
    # unpack unknowns
    unknowns   = segment.state.unknowns
    velocity_x = unknowns.velocity_x
    time       = unknowns.time
    
    # unpack givens
    v0         = segment.air_speed_start  
    t_initial  = segment.state.conditions.frames.inertial.time[0,0]
    t_nondim   = segment.state.numerics.dimensionless.control_points
    
    # time
    t_final    = t_initial + time  
    times      = t_nondim * (t_final-t_initial) + t_initial     

    #apply unknowns
    conditions = segment.state.conditions
    conditions.frames.inertial.velocity_vector[1:,0] = velocity_x
    conditions.frames.inertial.velocity_vector[0,0]  = v0
    conditions.frames.inertial.time[:,0]             = times[:,0]
