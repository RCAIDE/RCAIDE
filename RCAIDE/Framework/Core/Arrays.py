## @ingroup Core
# RCAIDE/Core/Arrays.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------      

import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  atleast_2d_col
# ----------------------------------------------------------------------------------------------------------------------        
## @ingroup Core
def atleast_2d_col(A):
    """Makes a 2D array in column format

    Assumptions:
        None

    Source:
        None

    Args:
        A  (numpy.ndarray):  1-D Array 

    Returns:
        A  (numpy.ndarray):  2-D Array  
    
    """       
    return atleast_2d(A,'col')


# ----------------------------------------------------------------------------------------------------------------------
#  atleast_2d_row
# ----------------------------------------------------------------------------------------------------------------------        
## @ingroup Core
def atleast_2d_row(A):
    """Makes a 2D array in row format

    Assumptions:
        None

    Source:
        None

    Args:
        A  (numpy.ndarray):  1-D Array 

    Returns:
        A  (numpy.ndarray):  2-D Array 

    """       
    return atleast_2d(A,'row')


# ----------------------------------------------------------------------------------------------------------------------
#  atleast_2d
# ----------------------------------------------------------------------------------------------------------------------        
## @ingroup Core
def atleast_2d(A,oned_as='row'):
    """ensures A is an array and at least of rank 2

    Assumptions:
        Defaults as row

    Source:
        None

    Args:
        A  (numpy.ndarray):  1-D Array 

    Returns:
        A  (numpy.ndarray):  2-D Array 

    """       
    
    # not an array yet
    if not isinstance(A,(np.ndarray,np.matrixlib.defmatrix.matrix)):
        if not isinstance(A,(list,tuple)):
            A = [A]
        A = np.array(A)
        
    # check rank
    if A.ndim < 2:
        # expand row or col
        if oned_as == 'row':
            A = A[None,:]
        elif oned_as == 'col':
            A = A[:,None]
        else:
            raise Exception("oned_as must be 'row' or 'col' ")
            
    return A


## @ingroup Core
def append_array(A=None,B=None):
    """ A stacking operation used by merged to put together data structures

        Assumptions:
            None

        Source:
            None

        Args:
            A (float)
            B (float)

        Returns:
            array
    """       
    if isinstance(A,np.ndarray) and isinstance(B,np.ndarray):
        return np.vstack([A,B])
    else:
        return None