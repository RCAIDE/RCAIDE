## @ingroup Methods-Missions-Segments-Common
# Numerics.py
# 
# Created:  Jul 2014, SUAVE Team
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from Legacy.trunk.S.Core.Arrays import atleast_2d_col 

# ----------------------------------------------------------------------
#  Initialize Differentials
# ----------------------------------------------------------------------

## @ingroup Methods-Missions-Segments-Common
def func_initialize_differentials_dimensionless(segment):
    """ Discretizes the differential operators
    
        Assumptions:
        N/A
        
        Inputs:
            state.numerics:
                number_control_points [int]
                discretization_method [function]
            
        Outputs:
            numerics.dimensionless:           
                control_points        [array]
                differentiate         [array]
                integrate             [array]

        Properties Used:
        N/A
                                
    """    
    
    
    # unpack
    numerics = segment.state.numerics
    N                     = numerics.number_control_points
    discretization_method = numerics.discretization_method
    
    # get operators
    x,D,I = discretization_method(N,**numerics)
    x = atleast_2d_col(x)
    
    # pack
    numerics.dimensionless.control_points = x
    numerics.dimensionless.differentiate  = D
    numerics.dimensionless.integrate      = I    
    
    return

# ----------------------------------------------------------------------
#  Update Differentials
# ----------------------------------------------------------------------

## @ingroup Methods-Missions-Segments-Common
def func_update_differentials_time(segment):
    """ Scales the differential operators (integrate and differentiate) based on mission time
    
        Assumptions:
        N/A
        
        Inputs:
            numerics.dimensionless:           
                control_points                    [array]
                differentiate                     [array]
                integrate                         [array]
            state.conditions.frames.inertial.time [seconds]
            
        Outputs:
            numerics.time:           
                control_points        [array]
                differentiate         [array]
                integrate             [array]

        Properties Used:
        N/A
                                
    """     
    
    # unpack
    numerics = segment.state.numerics
    x = numerics.dimensionless.control_points
    D = numerics.dimensionless.differentiate
    I = numerics.dimensionless.integrate
    
    # rescale time
    time = segment.state.conditions.frames.inertial.time
    T    = time[-1] - time[0]
    t    = x * T
    
    # rescale operators
    D = D / T
    I = I * T
    
    # pack
    numerics.time.control_points = t
    numerics.time.differentiate  = D
    numerics.time.integrate      = I

    return
    


initialize_differentials_dimensionless(State, Settings, System):
	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = func_initialize_differentials_dimensionless('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


update_differentials_time(State, Settings, System):
	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = func_update_differentials_time('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System