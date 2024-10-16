# RCAIDE/Library/Methods/Geometry/Two_Dimensional/Airfoil/import_airfoil_polars.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
from RCAIDE.Framework.Core import Data , Units

# python imports 
import RNUMPY as rp

# ----------------------------------------------------------------------------------------------------------------------
# Import Airfoil Polars 
# ----------------------------------------------------------------------------------------------------------------------   
def import_airfoil_polars(airfoil_polar_files, angle_of_attack_discretization = 89):
    """Imports airfoil polars from a text file
    
    Assumptions:
        Input airfoil polars file is obtained from XFOIL or from Airfoiltools.com
    
    Source:
        None 
    
    Args:
        airfoil polar files   (list): list of strings [-]
           
    Returns:
        airfoil_data
           .aoa_from_polar       (numpy.ndarray):  [radians]
           .re_from_polar        (numpy.ndarray):  [unitless]
           .mach_number          (numpy.ndarray):  [unitless]
           .lift_coefficients    (numpy.ndarray):  [unitless]
           .drag_coefficients    (numpy.ndarray):  [unitless]

    """      
     
    # number of airfoils   
    num_polars = 0 
    n_p = len(airfoil_polar_files)
    if n_p < 3:
        raise AttributeError('Provide three or more airfoil polars to compute surrogate') 
    num_polars            = max(num_polars, n_p)       
    
    # create empty data structures 
    AoA        = rp.zeros((num_polars, angle_of_attack_discretization))
    CL         = rp.zeros((num_polars, angle_of_attack_discretization))
    CD         = rp.zeros((num_polars, angle_of_attack_discretization))
    Re         = rp.zeros(num_polars)
    Ma         = rp.zeros(num_polars) 
    AoA_interp = rp.linspace(-6, 16, angle_of_attack_discretization)
    
    for j in range(len(airfoil_polar_files)):   
        # Open file and read column names and data block
        f = open(airfoil_polar_files[j]) 
        data_block = f.readlines()
        f.close()
        
        # Ignore header
        for header_line in range(len(data_block)):
            line = data_block[header_line]   
            if 'Re =' in line:    
                Re[j] = float(line[25:40].strip().replace(" ", ""))
            if 'Mach =' in line:    
                Ma[j] = float(line[7:20].strip().replace(" ", ""))    
            if '---' in line:
                data_block = data_block[header_line+1:]
                break
            
        # Remove any extra lines at end of file:
        last_line = False
        while last_line == False:
            if data_block[-1]=='\n':
                data_block = data_block[0:-1]
            else:
                last_line = True
        
        dim         = len(data_block)
        airfoil_AoA = rp.zeros(dim)
        airfoil_cl  = rp.zeros(dim)
        airfoil_cd  = rp.zeros(dim)     
    
        # Loop through each value: append to each column
        for line_count , line in enumerate(data_block):
            airfoil_AoA[line_count] = float(data_block[line_count][0:8].strip())
            airfoil_cl[line_count]  = float(data_block[line_count][10:17].strip())
            airfoil_cd[line_count]  = float(data_block[line_count][20:27].strip())   
      
        AoA[j,:] = AoA_interp
        CL[j,:]  = rp.interp(AoA_interp,airfoil_AoA,airfoil_cl)
        CD[j,:]  = rp.interp(AoA_interp,airfoil_AoA,airfoil_cd)  
    
    airfoil_data = Data()     
    airfoil_data.aoa_from_polar      = AoA*Units.degrees
    airfoil_data.re_from_polar       = Re   
    airfoil_data.mach_number         = Ma
    airfoil_data.lift_coefficients   = CL
    airfoil_data.drag_coefficients   = CD      
     
    return airfoil_data 