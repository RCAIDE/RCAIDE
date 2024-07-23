# RCAIDE/Library/Methods/Geometry/Two_Dimensional/Airfoil/compute_naca_4series.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team 
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    

from RCAIDE.Framework.Core import Data   
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  compute_naca_4series
# ----------------------------------------------------------------------------------------------------------------------   
def compute_naca_4series(airfoil_code,npoints= 201, leading_and_trailing_edge_resolution_factor = 1.5):
    """Computes the points of NACA 4-series airfoil

    Assumptions:
        None

    Source:
        None

    Args:
        airfoil_code                                (string): [-]
        npoints                                        (int): [unitless]    
        leading_and_trailing_edge_resolution_factor  (float): [unitless]

    Returns:
        airfoil_data
           .thickness_to_chord    (numpy.ndarray):  [unitless]
           .x_coordinates         (numpy.ndarray):  [meters]
           .y_coordinates         (numpy.ndarray):  [meters]
           .x_upper_surface       (numpy.ndarray):  [meters]
           .x_lower_surface       (numpy.ndarray):  [meters]
           .y_upper_surface       (numpy.ndarray):  [meters]
           .y_lower_surface       (numpy.ndarray):  [meters]
           .camber_coordinates    (numpy.ndarray):  [meters] 


    """
    if npoints%2 != 1:
        npoints+= 1
        print('Number of points must be odd, changing to ' + str(npoints) + ' points')  
         
    half_npoints    = npoints/2                                    
    airfoil_digits  = [int(x) for x in airfoil_code]
    camber          = airfoil_digits[0]/100                        # maximum camber as a fraction of chord
    camber_loc      = airfoil_digits[1]/10                         # maximum camber location as a fraction of chord
    thickness       = airfoil_digits[2]/10 + airfoil_digits[3]/100 # maximum thickness as a fraction of chord   
    x_us  = np.linspace(0,1,int(np.ceil(half_npoints)))   # number of points per side    
    x_ls  = np.linspace(0,1,int(np.ceil(half_npoints)))   
    if leading_and_trailing_edge_resolution_factor != None: 
        te = leading_and_trailing_edge_resolution_factor        # trailing-edge bunching factor 
        x_us  = 1 - (te+1)*x_us*(1-x_us)**te - (1-x_us)**(te+1) # bunched points, x, 0 to 1
        x_ls  = 1 - (te+1)*x_ls*(1-x_ls)**te - (1-x_ls)**(te+1) # bunched points, x, 0 to 1

    # normalized thickness, gap at trailing edge  
    t_ls = .2969*np.sqrt(x_ls) - 0.126*x_ls - 0.3516*(x_ls**2) + 0.2843*(x_ls**3) - 0.1015*(x_ls**4)
    t_us = .2969*np.sqrt(x_us) - 0.126*x_us - 0.3516*(x_us**2) + 0.2843*(x_us**3) - 0.1015*(x_us**4)
    t_ls = t_ls*thickness/.2
    t_us = t_us*thickness/.2 
    c_ls = camber/(1-camber_loc)**2 * ((1-2*camber_loc)+2*camber_loc*x_ls-x_ls**2)
    c_us = camber/(1-camber_loc)**2 * ((1-2*camber_loc)+2*camber_loc*x_us-x_us**2)
    
    if camber == 0 and camber_loc == 0:
        pass
    else:
        I_us = np.where(x_us<camber_loc)[0] 
        I_ls = np.where(x_ls<camber_loc)[0]  
        c_us[I_us] = camber/camber_loc**2*(2*camber_loc*x_us[I_us]-x_us[I_us]**2) 
        c_ls[I_ls] = camber/camber_loc**2*(2*camber_loc*x_ls[I_ls]-x_ls[I_ls]**2) 
    
    x_lo_surf = np.flip(x_ls)
    y_lo_surf = np.flip(c_ls - t_ls)
    y_up_surf = (c_us + t_us)[1:] 
    x_up_surf = x_us[1:]
   
    # concatenate upper and lower surfaces  
    y_data = np.hstack((y_lo_surf, y_up_surf)) 
    x_data = np.hstack((x_lo_surf,x_up_surf)) 
    
    # get airfoil properties 
    max_t  = np.max(thickness)
    max_c  = max(x_data) - min(x_data)
    t_c    = max_t/max_c         

    airfoil_data                    = Data()    
    airfoil_data.max_thickness      = max_t 
    airfoil_data.x_coordinates      = x_data   
    airfoil_data.y_coordinates      = y_data      
    airfoil_data.x_upper_surface    = x_us 
    airfoil_data.x_lower_surface    = x_ls 
    airfoil_data.y_upper_surface    = np.append(0,y_up_surf) 
    airfoil_data.y_lower_surface    = y_lo_surf[::-1]           
    airfoil_data.camber_coordinates = camber         
    airfoil_data.thickness_to_chord = t_c 
    
    return airfoil_data