## @ingroup Library-Methods-Mission-Common-Initialize
# RCAIDE/Library/Methods/Missions/Common/Initialize/differentials_dimensionless.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE Imports 
from RCAIDE.Framework.Core.Arrays  import atleast_2d_col

# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Differentials
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Mission-Common-Initialize
def differentials_dimensionless(segment):
    """ Discretizes the differential operators
    
        Assumptions:
        N/A
        
        Inputs:
            state.numerics:
                number_of_control_points [int]
                discretization_method    [function]
            
        Outputs:
            numerics.dimensionless:            
                control_points           [array]
                differentiate            [array]
                integrate                [array]

        Properties Used:
        N/A
                                
    """     
    
    # unpack
    numerics              = segment.state.numerics
    N                     = numerics.number_of_control_points
    discretization_method = numerics.discretization_method
    
    # get operators
    x,D,I = discretization_method(N,**numerics)
    x = atleast_2d_col(x)
    
    # pack
    numerics.dimensionless.control_points = x
    numerics.dimensionless.differentiate  = D
    numerics.dimensionless.integrate      = I    
    
    return
 


def _differentials_dimensionless(State, Settings, System):
	'''
	Framework version of differentials_dimensionless.
	Wraps differentials_dimensionless with State, Settings, System pack/unpack.
	Please see differentials_dimensionless documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = differentials_dimensionless('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System