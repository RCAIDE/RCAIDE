
# optimize.py
# 
# Created: Dec 2016, RCAIDE Team
# Modified:
#           Mar 2020, M. Clarke
#           Apr 2020, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import scipy.optimize as opt
import numpy as np  

# ----------------------------------------------------------------------
#  Converge Root
# ----------------------------------------------------------------------
def converge_opt(segment):
    """Interfaces the mission to an optimization algorithm

    Assumptions:
    None

    Source:
    None

    Args:
    state.unknowns                     [Data]
    segment                            [Data]
    segment.algorithm                  [string]

    Returns:
    state.unknowns                     [Any]


    """     
    
    # pack up the array
    unknowns = segment.state.unknowns.pack_array()
    
    # Have the optimizer call the wrapper
    obj       = lambda unknowns:get_objective(unknowns,segment)   
    econ      = lambda unknowns:get_econstraints(unknowns,segment) 
    iecon     = lambda unknowns:get_ieconstraints(unknowns,segment)
    
    # Setup the bnds of the problem
    bnds = make_bnds(unknowns, segment)
    
    # Solve the problem, based on chosen algorithm
    if segment.algorithm == 'SLSQP':
        unknowns = opt.fmin_slsqp(obj,unknowns,f_eqcons=econ,f_ieqcons=iecon,bounds=bnds,iter=2000)
    return
    
# ----------------------------------------------------------------------
#  Helper Functions
# ----------------------------------------------------------------------
    

def get_objective(unknowns, segment):
    """ Runs the mission if the objective value is needed
    
        Assumptions:
        None
        
        Args:
        state.unknowns      [Data]
    
        Returns:
        objective           [float]

        
                                
    """      
    
    if isinstance(unknowns,np.ndarray):
        segment.state.unknowns.unpack_array(unknowns)
    else:
        segment.state.unknowns = unknowns
        
    if not np.all(segment.state.inputs_last == segment.state.unknowns):       
        segment.process.iterate(segment)
        
    objective = segment.state.objective_value
    
    return objective


def get_econstraints(unknowns, segment):
    """ Runs the mission if the equality constraint values are needed
    
        Assumptions:
        None
        
        Args:
        state.unknowns      [Data]
            
        Returns:
        constraints          [array]

        
                                
    """       
    
    if isinstance(unknowns,np.ndarray):
        segment.state.unknowns.unpack_array(unknowns)
    else:
        segment.state.unknowns = unknowns
        
    if not np.all(segment.state.inputs_last == segment.state.unknowns):       
        segment.process.iterate(segment)

    constraints = segment.state.constraint_values
    
    return constraints


def make_bnds(unknowns, segment):
    """ Automatically sets the bounds of the optimization.
    
        Assumptions:
        Restricts throttle to between 0 and 100%
        Restricts body angle from 0 to pi/2 radians
        Restricts flight path angle from 0 to pi/2 radians
        
        Args:
        none
            
        Returns:
        bnds

        
                                
    """      

    ones    = segment.state.ones_row(1)
    ones_m1 = segment.state.ones_row_m1(1).resize(segment.state._size)
    ones_m2 = segment.state.ones_row_m2(1).resize(segment.state._size)
    
    throttle_bnds = ones*(0.,1.)
    body_angle    = ones*(0., np.pi/2.)
    gamma         = ones*(0., np.pi/2.)
    
    if segment.air_speed_end is None:
        vels      = ones_m1*(0.,2000.)
    elif segment.air_speed_end is not None:    
        vels      = ones_m2*(0.,2000.)
    
    bnds = np.vstack([throttle_bnds,gamma,body_angle,vels])
    
    bnds = list(map(tuple, bnds))
    
    return bnds


def get_ieconstraints(unknowns, segment):
    """ Runs the mission if the inequality constraint values are needed, these are specific to a climb
    
        Assumptions:
        Time only goes forward
        CL is less than a specified limit
        CL is greater than zero
        All altitudes are greater than zero
        The vehicle accelerates not decelerates
        
        Args:
        state.unknowns      [Data]
            
        Returns:
        constraints          [array]

        
                                
    """      

    if isinstance(unknowns,np.ndarray):
        segment.state.unknowns.unpack_array(unknowns)
    else:
        segment.state.unknowns = unknowns
        
    if not np.all(segment.state.inputs_last == segment.state.unknowns):
        segment.process.iterate(segment)
    
    # Time goes forward, not backward
    t_final = segment.state.conditions.frames.inertial.time[-1,0]
    time_con = (segment.state.conditions.frames.inertial.time[1:,0] - segment.state.conditions.frames.inertial.time[0:-1,0])/t_final
    
    # Less than a specified CL limit
    lift_coefficient_limit = segment.lift_coefficient_limit
    CL_con   = (lift_coefficient_limit  - segment.state.conditions.aerodynamics.coefficients.lift.total[:,0])/lift_coefficient_limit 
    CL_con2  = segment.state.conditions.aerodynamics.coefficients.lift.total[:,0]
    
    # Altitudes are greater than 0
    alt_con = segment.state.conditions.freestream.altitude[:,0]/segment.altitude_end
    
    # Acceleration constraint, go faster not slower
    acc_con   = segment.state.conditions.frames.inertial.acceleration_vector[:,0]
    
    constraints = np.concatenate((time_con,CL_con,CL_con2,alt_con,acc_con))
    
    return constraints 