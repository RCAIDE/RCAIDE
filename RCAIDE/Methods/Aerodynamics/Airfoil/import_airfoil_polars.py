## @ingroup Methods-Aerodynamics-Airfoil
# import_airfoil_polars.py
# 
# Created:  Oct 2023, Racheal M. Erhard

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
from Legacy.trunk.S.Core import Data, Units 
import numpy as np

## @ingroup Methods-Aerodynamics-Airfoil
def import_airfoil_polars(airfoil_analysis):
    """This is a direct import of airfoil polars from a text file.
    
    Assumptions:
    The text file is assumed to be in the same format as an output polar file from XFOIL or Airfoiltools.com.
    
    Source:
    N/A
    
    Inputs:
    airfoil_analysis                             -  The airfoil analysis class with all settings
       .angle_of_attack_discretization           -  Number of angles of attack over which to interpolate from the 
                                                      direct data. This is required if more than one polar is analyzed, 
                                                      as the output structure is assumed to have the same shape.
       .interpolated_angle_of_attack_lower_bound -  Lower bound on interpolated angle of attack
       .interpolated_angle_of_attack_upper_bound -  Upper bound on interpolated angle of attack
       .polar_files                              -  Paths to each polar file used in analysis      <list of strings>
                                             
    
    Outputs:
    data       numpy array with airfoil data
    
    Properties Used:
    N/A
    """  
    # Extract settings from the airfoil analysis
    aoa_discretization = airfoil_analysis.settings.polar_import_method.angle_of_attack_discretization
    aoa_interpolated_lb = airfoil_analysis.settings.polar_import_method.interpolated_angle_of_attack_lower_bound
    aoa_interpolated_ub = airfoil_analysis.settings.polar_import_method.interpolated_angle_of_attack_upper_bound
    airfoil_polar_files = airfoil_analysis.settings.polar_import_method.polar_files
    
    # number of airfoils   
    num_polars = len(airfoil_polar_files)
    if num_polars < 3:
        raise AttributeError('Provide three or more airfoil polars to compute surrogate')     
    
    # create empty data structures 
    airfoil_data = Data() 
    AoA = np.zeros((num_polars, aoa_discretization))
    CL = np.zeros((num_polars, aoa_discretization))
    CD = np.zeros((num_polars, aoa_discretization)) 
    Re = np.zeros(num_polars)
    Ma = np.zeros(num_polars)
    
    AoA_interp = np.linspace(aoa_interpolated_lb, aoa_interpolated_ub, aoa_discretization)  
    
    for j in range(len(airfoil_polar_files)):   
        # Open file and parse data block
        data_block, Re[j], Ma[j] = parse_data_from_file(airfoil_polar_files[j])

        data_len = len(data_block)
        airfoil_aoa = np.zeros(data_len)
        airfoil_cl = np.zeros(data_len)
        airfoil_cd = np.zeros(data_len)     
    
        # Loop through each value: append to each column
        for line_count , line in enumerate(data_block):
            airfoil_aoa[line_count] = float(data_block[line_count][0:8].strip())
            airfoil_cl[line_count] = float(data_block[line_count][10:17].strip())
            airfoil_cd[line_count] = float(data_block[line_count][20:27].strip())   
      
        AoA[j,:] = AoA_interp
        CL[j,:]  = np.interp(AoA_interp, airfoil_aoa, airfoil_cl)
        CD[j,:]  = np.interp(AoA_interp, airfoil_aoa, airfoil_cd)  
    
    airfoil_data.aoa_from_polar = AoA * Units.degrees
    airfoil_data.re_from_polar = Re   
    airfoil_data.mach_number = Ma
    airfoil_data.lift_coefficients = CL
    airfoil_data.drag_coefficients = CD      
     
    return airfoil_data 


## @ingroup Methods-Aerodynamics-Airfoil
def parse_data_from_file(airfoil_polar_file):
    f = open(airfoil_polar_file) 
    data_block = f.readlines()
    f.close()
    
    # Ignore header
    for header_line in range(len(data_block)):
        line = data_block[header_line]   
        if 'Re =' in line:    
            Re = float(line[25:40].strip().replace(" ", ""))
        if 'Mach =' in line:    
            Ma = float(line[7:20].strip().replace(" ", ""))    
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
    return data_block, Re, Ma