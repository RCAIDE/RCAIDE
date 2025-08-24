# RCAIDE/Library/Methods/Stability/Moment_of_Inertia/compute_rounded_end_cylinder_moment_of_inertia.py 
# 
# Created:  Aug. 2025, M. Clarke  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Rounded-End Cylinder Moment of Intertia
# ----------------------------------------------------------------------------------------------------------------------   
def compute_rounded_end_cylinder_moment_of_inertia(origin,mass,outer_length,outer_radius,inner_length = 0,inner_radius = 0,center_of_gravity = np.array([[0,0,0]])):  
    ''' computes the moment of inertia tensor for a hollow rounded end cylinder

    Assumptions:
    - Cylinder has a constant density
    - Cylinder has a rounded end 
    - Origin is at the center of the cylinder
    - Cylinder axis of rotation is along the x-axis

    Source: 
 
    Inputs:
    - Component properties (origin, mass, outer_length, outer_radius)
    - Center of gravity

    Outputs:
    - cylinder moment of inertia tensor

    Properties Used:
    N/A
    '''
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # Setup
    # ----------------------------------------------------------------------------------------------------------------------           
    I =  np.zeros((3, 3))
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # Moment of inertia in local system 
    # ----------------------------------------------------------------------------------------------------------------------
    
    # Avoid divide by zero error for a point mass
    if  (outer_radius == 0 or outer_length == 0):
        volume = 1
    else:
        outer_volume = (np.pi * outer_radius ** 2 * outer_length ) + ( 4 / 3 * np.pi * outer_radius ** 3)
        inner_volume = (np.pi * inner_radius ** 2 * inner_length ) + ( 4 / 3 * np.pi * inner_radius ** 3) 
        volume = outer_volume - inner_volume
        
    rho     = mass / volume
    #I[0][0] = # WRONG rho * (1 / 2 * np.pi * (outer_radius ** 4 * outer_length) - 1 / 2 * np.pi * (inner_radius ** 4 * inner_length)) # Ixx
    #I[1][1] = # WRONG rho * (1 / 12 * (3 *np.pi*(outer_radius ** 4)*outer_length + np.pi * outer_radius ** 2 * outer_length ** 2) - 1 / 12 * (3 * (inner_radius ** 4) *np.pi *inner_length + np.pi * inner_radius ** 2 * inner_length ** 2)) # Iyy
    #I[2][2] = # WRONG rho * (1 / 12 * (3 *np.pi*(outer_radius ** 4)*outer_length + np.pi * outer_radius ** 2 * outer_length ** 2) - 1 / 12 * (3 * (inner_radius ** 4) *np.pi *inner_length + np.pi * inner_radius ** 2 * inner_length ** 2)) # Izz
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # transform moment of inertia to the global system
    # ----------------------------------------------------------------------------------------------------------------------
    s        = np.array(center_of_gravity) - np.array(origin) # Vector between component and the CG    
    I_global = np.array(I) + mass * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - s*np.transpose(s))
    
    return I_global,  mass