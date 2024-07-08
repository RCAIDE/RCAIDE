# RCAIDE/Library/Methods/Geometry/Airfoil/import_airfoil_dat.py
# (c) Copyright 2023 Aerospace Research Community LLC

# Created: Jul 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
# IMPORTS 
# ----------------------------------------------------------------------------------------------------------------------      

import numpy as np

# ----------------------------------------------------------------------------------------------------------------------  
#  import airfoil dat
# ----------------------------------------------------------------------------------------------------------------------  
def import_airfoil_dat(filename):
    """Import an airfoil data file and stores it in a numpy array.
    
    Assumptions:
    Airfoil file in Lednicer format

    Source:
    None

    Args:
    filename   <string>

    Returns:
    data       numpy array with airfoil data 
    """     
    
    filein = open(filename,'r')
    data = {}   
    data['header'] = filein.readline().strip() + filein.readline().strip()

    filein.readline()
    
    sections = ['upper','lower']
    data['upper'] = []
    data['lower'] = []
    section = None
    
    while True:
        line = filein.readline()
        if not line: 
            break
        
        line = line.strip()
        
        if line and section:
            pass
        elif not line and not section:
            continue
        elif line and not section:
            section = sections.pop(0)
        elif not line and section:
            section = None
            continue
        
        point = list(map(float,line.split()))
        data[section].append(point)
        
    for k,v in data.items():
        data[k] = np.array(v)
        
    return data