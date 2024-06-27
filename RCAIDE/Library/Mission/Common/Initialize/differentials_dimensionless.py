## @ingroup Library-Missions-Common-Initialize
# RCAIDE/Library/Missions/Common/Initialize/differentials_dimensionless.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE Imports 
from RCAIDE.Framework.Core.Arrays  import atleast_2d_col 

# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Differentials
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Missions-Common-Initialize
def differentials_dimensionless(segment):
    """ Discretizes the differential operators based on the discretization method chosen
    
        Assumptions:
            None 
        
        Args: 
            segment  : flight segment        [-] 
            
        Returns:
            None 
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
 