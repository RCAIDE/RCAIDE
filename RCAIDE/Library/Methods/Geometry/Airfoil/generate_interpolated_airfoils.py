# RCAIDE/Library/Methods/Geometry/Two_Dimensional/Airfoil/generate_interpolated_airfoils.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team 
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
from Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Cross_Section.Airfoil import import_airfoil_geometry  

# python imports 
import numpy as np
import os

# ----------------------------------------------------------------------------------------------------------------------
#  generate_interpolated_airfoils
# ----------------------------------------------------------------------------------------------------------------------   
def generate_interpolated_airfoils(airfoil_1, airfoil_2, nairfoils, npoints=201, save_filename="airfoil"):
    """ Takes in two airfoils, interpolates between their coordinates to generate new
    airfoil geometries and saves new airfoil files.
    
    Assumptions:
        Linear geometric transition between airfoils
    
    Source: 
        None
    
    Args:
        airfoil_1      (string): filepath to first airfoil            [-]
        airfoil_2      (string): filepath to second airfoil           [-]
        nairfoils         (int): number of airfoils                   [unitless]
        npoints           (int): number of points on airfoil          [unitless]
        save_filename  (string): filename of interpolated airfoil(s)  [-]
    
    """ 
    # for each point around the airfoil, interpolate between the two given airfoil coordinates 
    a_geo_1  = import_airfoil_geometry(airfoil_1,npoints)    
    y_u_lb   = a_geo_1.y_upper_surface 
    y_u_ub   = a_geo_2.y_upper_surface 
    y_l_lb   = a_geo_1.y_lower_surface 
    y_l_ub   = a_geo_2.y_lower_surface      

    a_geo_2  = import_airfoil_geometry(airfoil_2,npoints)     
    x_u_lb   = a_geo_1.x_upper_surface 
    x_u_ub   = a_geo_2.x_upper_surface 
    x_l_lb   = a_geo_1.x_lower_surface 
    x_l_ub   = a_geo_2.x_lower_surface     
    
    # broadcasting interpolation
    z         = np.linspace(0,1,nairfoils)
    y_n_upper = (z[None,...] * (y_u_ub[...,None] - y_u_lb[...,None]) + (y_u_lb[...,None])).T
    y_n_lower = (z[None,...] * (y_l_ub[...,None] - y_l_lb[...,None]) + (y_l_lb[...,None])).T
    x_n_upper = (z[None,...] * (x_u_ub[...,None] - x_u_lb[...,None]) + (x_u_lb[...,None])).T
    x_n_lower = (z[None,...] * (x_l_ub[...,None] - x_l_lb[...,None]) + (x_l_lb[...,None])).T
    
    
    # save new airfoil geometry files:
    new_files     = {'airfoil_{}'.format(i+1): [] for i in range(nairfoils-2)}
    airfoil_files = []

    # import airfoil geometry for the two airfoils 
    airfoil_1_name = os.path.basename(airfoil_1)
    airfoil_2_name = os.path.basename(airfoil_2)
    for j in range(nairfoils-2):
        # create new files and write title block for each new airfoil
        title_block     = "Airfoil Transition "+str(j+1)+" between "+airfoil_1_name+" and "+airfoil_2_name+"\n 61. 61.\n\n"
        file            ='airfoil_'+str(j+1)
        new_files[file] = open(save_filename  + "_" + str(j+1) +".txt", "w+")
        new_files[file].write(title_block)
        
        y_n_u = np.reshape(y_n_upper[j+1],(npoints//2,1))
        y_n_l = np.reshape(y_n_lower[j+1],(npoints//2,1))
        x_n_u = np.reshape(x_n_upper[j+1],(npoints//2,1))
        x_n_l = np.reshape(x_n_lower[j+1],(npoints//2,1))
        
        airfoil_files.append(new_files[file].name)
        upper_data = np.append(x_n_u, y_n_u,axis=1)
        lower_data = np.append(x_n_l, y_n_l,axis=1)

        # write lines to files
        for lines in upper_data: #upper_data[file]:
            line = str(lines[0]) + " " + str(lines[1]) + "\n"
            new_files[file].write(line) 
        new_files[file].write("\n")
        
        for lines in lower_data: #[file]:
            line = str(lines[0]) + " " + str(lines[1]) + "\n"
            new_files[file].write(line) 
        new_files[file].close() 
    
    return new_files
