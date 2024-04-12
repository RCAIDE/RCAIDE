## @ingroup Methods-Geometry-Three_Dimensional
#
# Created:   
# Modified: Jan 2020, M. Clarke

import numpy as np
from .orientation_product import orientation_product

## @ingroup Methods-Geometry-Three_Dimensional
def func_angles_to_dcms(rotations,sequence=(2,1,0)):
    """Builds an euler angle rotation matrix
    
    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    rotations     [radians]  [r1s r2s r3s], column array of rotations
    sequence      [-]        (2,1,0) (default), (2,1,2), etc.. a combination of three column indices

    Outputs:
    transform     [-]        3-dimensional array with direction cosine matrices
                             patterned along dimension zero

    Properties Used:
    N/A
    """         
    # transform map
    Ts = { 0:T0, 1:T1, 2:T2 }
    
    # a bunch of eyes
    transform = new_tensor(rotations[:,0])
    
    # build the tranform
    for dim in sequence[::-1]:
        angs = rotations[:,dim]
        transform = orientation_product( transform, Ts[dim](angs) )
    
    # done!
    return transform
  
## @ingroup Methods-Geometry-Three_Dimensional
def func_T0(a):
    """Rotation matrix about first axis
    
    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    a        [radians] angle of rotation

    Outputs:
    T        [-]       rotation matrix

    Properties Used:
    N/A
    """      
    # T = np.array([[1,   0,  0],
    #               [0, cos,sin],
    #               [0,-sin,cos]])
    
    cos = np.cos(a)
    sin = np.sin(a)
                  
    T = new_tensor(a)
    
    T[:,1,1] = cos
    T[:,1,2] = sin
    T[:,2,1] = -sin
    T[:,2,2] = cos
    
    return T
        
## @ingroup Methods-Geometry-Three_Dimensional
def func_T1(a):
    """Rotation matrix about second axis
    
    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    a        [radians] angle of rotation

    Outputs:
    T        [-]       rotation matrix

    Properties Used:
    N/A
    """      
    # T = np.array([[cos,0,-sin],
    #               [0  ,1,   0],
    #               [sin,0, cos]])
    
    cos = np.cos(a)
    sin = np.sin(a)     
    
    T = new_tensor(a)
    
    T[:,0,0] = cos
    T[:,0,2] = -sin
    T[:,2,0] = sin
    T[:,2,2] = cos
    
    return T

## @ingroup Methods-Geometry-Three_Dimensional
def func_T2(a):
    """Rotation matrix about third axis
    
    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    a        [radians] angle of rotation

    Outputs:
    T        [-]       rotation matrix

    Properties Used:
    N/A
    """      
    # T = np.array([[cos ,sin,0],
    #               [-sin,cos,0],
    #               [0   ,0  ,1]])
        
    cos = np.cos(a)
    sin = np.sin(a)     
    
    T = new_tensor(a)
    
    T[:,0,0] = cos
    T[:,0,1] = sin
    T[:,1,0] = -sin
    T[:,1,1] = cos
        
    return T

## @ingroup Methods-Geometry-Three_Dimensional
def func_new_tensor(a):
    """Initializes the required tensor. Able to handle imaginary values.
    
    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    a        [radians] angle of rotation

    Outputs:
    T        [-]       3-dimensional array with identity matrix
                       patterned along dimension zero

    Properties Used:
    N/A
    """      
    assert a.ndim == 1
    n_a = len(a)
    
    T = np.eye(3)
    
    if a.dtype is np.dtype('complex'):
        T = T + 0j
    
    T = np.resize(T,[n_a,3,3])
    
    return T    


angles_to_dcms(State, Settings, System):
	#TODO: rotations = [Replace With State, Settings, or System Attribute]
	#TODO: sequence  = [Replace With State, Settings, or System Attribute]

	results = func_angles_to_dcms('rotations', 'sequence')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


T0(State, Settings, System):
	#TODO: a = [Replace With State, Settings, or System Attribute]

	results = func_T0('a',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


T1(State, Settings, System):
	#TODO: a = [Replace With State, Settings, or System Attribute]

	results = func_T1('a',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


T2(State, Settings, System):
	#TODO: a = [Replace With State, Settings, or System Attribute]

	results = func_T2('a',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


new_tensor(State, Settings, System):
	#TODO: a = [Replace With State, Settings, or System Attribute]

	results = func_new_tensor('a',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System