# load.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------      

import json
import pickle
from RCAIDE.Frameworks.Core import Data, DataOrdered
import numpy as np
from collections import OrderedDict

# ----------------------------------------------------------------------------------------------------------------------
#  load
# ----------------------------------------------------------------------------------------------------------------------    
def json_load(filename):
    """Converts a JSON file into a RCAIDE data structure.

    Assumptions:
    JSON file was a previously saved RCAIDE data structure.

    Source:
    N/A

    Inputs:
    filename   <string> - file to be loaded

    Outputs:
    data       RCAIDE data structure

    Properties Used:
    N/A
    """ 
    
    # Get JSON string
    f = open(filename)
    res_string = f.readline()
    f.close()    
    
    # Convert to dictionary
    res_dict = json.loads(res_string,object_pairs_hook=OrderedDict)    
    
    # Convert to RCAIDE data structure
    data = read_RCAIDE_json_dict(res_dict) 
    
    return data
 
def pickle_load(filename):
    """Converts a  pickle file into a RCAIDE data structure.

    Assumptions:
    pickle file was a previously saved RCAIDE data structure.

    Source:
    N/A

    Inputs:
    filename   <string> - file to be loaded

    Outputs:
    data       RCAIDE data structure

    Properties Used:
    N/A
    """  
    load_file = filename + '.pkl' 
    with open(load_file, 'rb') as file:
        data = pickle.load(file)   
    
    return data

def read_RCAIDE_json_dict(res_dict):
    """Builds a RCAIDE data structure based on a dictionary from a JSON file. This is initial case.

    Assumptions:
    Dictionary was created based on a previously saved RCAIDE data structure.

    Source:
    N/A

    Inputs:
    res_dict    Dictionary based on the RCAIDE data structure

    Outputs:
    RCAIDE_data  RCAIDE data structure

    Properties Used:
    N/A
    """      
    keys = res_dict.keys() # keys from top level
    RCAIDE_data = Data() # initialize RCAIDE data structure
    
    # Assign all values
    for k in keys:
        k = str(k)
        v = res_dict[k]
        RCAIDE_data[k] = build_data_r(v) # recursive function
    return RCAIDE_data
 
def build_data_r(v):
    """Builds a RCAIDE data structure based on a dictionary from a JSON file. This is recursive step.

    Assumptions:
    Dictionary was created based on a previously saved RCAIDE data structure.

    Source:
    N/A

    Inputs:
    v     generic value

    Outputs:
    ret   value converted to needed format

    Properties Used:
    N/A
    """          
    tv = type(v) # Get value type
    
    # Transform to RCAIDE data structure with appropriate types
    if tv == OrderedDict:
        keys = v.keys()
        # Recursively assign values
        ret = DataOrdered()
        for k in keys:
            k = str(k)
            ret[k] = build_data_r(v[k])
    elif tv == list:
        ret = np.array(v)
    elif (tv == str): 
        ret = str(v)
    elif (tv == bool):
        ret = v
    elif tv == type(None):
        ret = None
    elif (tv == float) or (tv == int):
        ret = v        
    else:
        raise TypeError('Data type not expected in RCAIDE JSON structure')

    return ret