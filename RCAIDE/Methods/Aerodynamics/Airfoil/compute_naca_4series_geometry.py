## @ingroup Methods-Aerodynamics-Airfoil
# compute_naca_4series_geometry.py
#
# Created:  Oct 2023, Racheal M. Erhard
# Modified: 
#           

from RCAIDE.Core import Data   
import numpy as np


## @ingroup Methods-Aerodynamics-Airfoil
def compute_naca_4series_geometry(airfoil):
    """Computes the points of NACA 4-series airfoil

    Assumptions:
    None

    Source:
    None

    Inputs:
        airfoil.                       airfoil component data structure
           settings.NACA_4_series_digits  - The 4-digit description of the NACA 4 series airfoil
           settings.number_of_points      - The number of discretization points around the airfoil geometry
           settings.leading_and_trailing_edge_resolution_factor - The LE and TE resolution factor
           
    Outputs:
    airfoil_data.
        thickness_to_chord                           [unitless]
        x_coordinates                                [meters]
        y_coordinates                                [meters]
        x_upper_surface                              [meters]
        x_lower_surface                              [meters]
        y_upper_surface                              [meters]
        y_lower_surface                              [meters]
        camber_coordinates                           [meters] 

    Properties Used:
    N/A
    """   
    # Extract data from airfoil component settings
    airfoil_name = airfoil.settings.NACA_4_series_digits
    npoints = airfoil.settings.number_of_points
    res_factor = airfoil.settings.leading_and_trailing_edge_resolution_factor # points per side and trailing-edge bunching factor 
    
    # Extract geometric parameters from 4series digits
    geometry        = Data()
    half_npoints    = npoints/2                                        # number of points per side of airfoil  
    airfoil_digits  = [int(x) for x in airfoil_name]
    camber          = airfoil_digits[0] / 100                          # maximum camber as a fraction of chord
    camber_loc      = airfoil_digits[1] / 10                           # maximum camber location as a fraction of chord
    thickness       = airfoil_digits[2] / 10 + airfoil_digits[3] / 100 # maximum thickness as a fraction of chord  
    
    # Get upper and lower surface x
    x_us  = np.linspace(0,1,int(np.ceil(half_npoints))+ (npoints%2 == 0))  
    x_ls  = np.linspace(0,1,int(np.ceil(half_npoints)))
    x_us  = resolution(x_us, res_factor)    # bunched points, x, 0 to 1
    x_ls  = resolution(x_ls, res_factor)    # bunched points, x, 0 to 1

    # Get normalized thickness, with gap at trailing edge  
    t_us = thickness_calculation(x_us, thickness)
    t_ls = thickness_calculation(x_ls, thickness)
    
    # Get camber
    c_us = camber_calculation(x_us, camber, camber_loc)
    c_ls = camber_calculation(x_ls, camber, camber_loc)
    
    # Surface positions
    x_up_surf = x_us[1:]
    x_lo_surf = np.flip(x_ls)
    y_up_surf = (c_us + t_us)[1:] 
    y_lo_surf = np.flip(c_ls - t_ls)
   
    # Concatenate upper and lower surfaces  
    x_data = np.hstack((x_lo_surf,x_up_surf))
    y_data = np.hstack((y_lo_surf, y_up_surf))  
    
    # 
    max_t  = np.max(thickness)
    max_c  = max(x_data) - min(x_data)
    t_c    = max_t/max_c         
    
    geometry.max_thickness      = max_t 
    geometry.x_coordinates      = x_data   
    geometry.y_coordinates      = y_data      
    geometry.x_upper_surface    = x_us 
    geometry.x_lower_surface    = x_ls 
    geometry.y_upper_surface    = np.append(0,y_up_surf) 
    geometry.y_lower_surface    = y_lo_surf[::-1]           
    geometry.camber_coordinates = camber         
    geometry.thickness_to_chord = t_c 
    
    return geometry


## @ingroup Methods-Aerodynamics-Airfoil
def resolution(x, te):
    return 1 - (te + 1) * x * (1 - x)**te - (1 - x)**(te + 1)


## @ingroup Methods-Aerodynamics-Airfoil
def thickness_calculation(x, thickness):
    """
    Calculates the thickness for a symmetrical 4-digit NACA airfoil.
    
    Inputs
       x         - position along the chord from 0 to 1           [-]
       thickness - maximum thickness as a fraction of the chord   [-]
    Outputs
       y         - half the thickness at each input position x
       
    Source
       "An introduction to theoretical and computational aerodynamics", Jack Moran.
       
    """
    return (0.2969*np.sqrt(x) - 0.126*x - 0.3516*(x**2) + 0.2843*(x**3) - 0.1015*(x**4) ) * thickness * 5.0


## @ingroup Methods-Aerodynamics-Airfoil
def camber_calculation(x, m, p):
    """
    Calculates the mean camber line for a 4-digit NACA airfoil.
    
    Inputs
       x   - position along the chord from 0 to 1 [-]
       m   - maximum camber
       p   - position of maximum camber
    
    Source
       "An introduction to theoretical and computational aerodynamics", Jack Moran.
       
    """
    # Equation for camber aft the max camber location
    yc = m / (1 - p) **2 * ((1 - 2 * p) + 2 * p * x - x**2)

    # Equation for camber before the max camber location
    if np.any(x < p):
        I = np.where(x < p)[0]
        yc[I] = m / p**2 * (2 * p * x[I] - x[I]**2) 

    return yc