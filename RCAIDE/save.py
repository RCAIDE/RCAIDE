# save.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------      

import numpy as np
import types
import json
import pickle
from collections import OrderedDict

# ----------------------------------------------------------------------------------------------------------------------
#  save
# ----------------------------------------------------------------------------------------------------------------------       
def json_save(data,filename):
    """Converts a RCAIDE data structure to a JSON file for storage. 

    Assumptions:
    Data must be numpy arrays, strings, booleans, floats, ints, or lists.
    Functions are ignored and all other data raises an error.

    Source:
    N/A

    Inputs:
    data       RCAIDE data structure
    filename   <string> - file to be output

    Outputs:

    Properties Used:
    N/A
    """      
    # Create a dictionary structure with the results
    res_dict = build_dict_base(data)
    
    # Convert the dictionary to a JSON string
    res_string = json.dumps(res_dict)
    
    # Write results to a file
    f = open(filename,'w')   
    f.write(res_string)
    f.close()  
    return 

def pickle_save(data,filename):
    """Converts a RCAIDE data structure to a pickle file for storage. 

    Assumptions:
    Data must be numpy arrays, strings, booleans, floats, ints, or lists.
    Functions are ignored and all other data raises an error.

    Source:
    N/A

    Inputs:
    data       RCAIDE data structure
    filename   <string> - file to be output

    Outputs:

    Properties Used:
    N/A
    """      
    pickle_file  =  filename + '.pkl'
    with open(pickle_file, 'wb') as file:
        pickle.dump(data, file) 
    return  
        
def build_dict_base(base):
    """Builds a dictionary based on a RCAIDE data structure. This is initial case.

    Assumptions:
    Data must be numpy arrays, strings, booleans, floats, ints, or lists.
    Functions are ignored and all other data raises an error.

    Source:
    N/A

    Inputs:
    data       RCAIDE data structure

    Outputs:
    base_dict  Dictionary built on the data structure.

    Properties Used:
    N/A
    """      
    
    keys = base.keys() # keys from top level
    base_dict = OrderedDict() # initialize dictionary
    # Ordered is used because some post processing currently
    # relies on the segments being in order
    
    # Assign all values
    for k in keys:
        v = base[k]
        base_dict[k] = build_dict_r(v) # recursive function
    return base_dict
     
def build_dict_r(v):
    """Builds a dictionary based on a RCAIDE data structure. This the recursive step.

    Assumptions:
    Data must be numpy arrays, strings, booleans, floats, ints, or lists.
    Functions are ignored and all other data raises an error.

    Source:
    N/A

    Inputs:
    v       value in a data structure

    Outputs:
    ret     value based on type of v

    Properties Used:
    N/A
    """      
    tv = type(v) # Get value type
    
    # Transform to basic python data type as appropriate
    if (tv == np.ndarray) or (tv == np.float64):
        ret = v.tolist()
    elif (tv == str) or (tv == bool):
        ret = v
    elif tv == type(None):
        ret = None
    elif (tv == float) or (tv == int):
        ret = v
    elif tv == types.FunctionType: # Functions cannot be stored
        ret = None        
    elif tv == list:
        ret = v    

    else:
        # Assume other data types are RCAIDE data types and check
        try:
            keys = v.keys()
        except:
            if callable(tv):
                return None
            else:
                raise TypeError('Unexpected data type in RCAIDE data structure')
        # Recursively assign values
        ret = OrderedDict()
        for k in keys:
            ret[k] = build_dict_r(v[k])        
    
    return ret