# RCAIDE/Library/Methods/Mass_Properties/Moment_of_Inertia/compute_cabin_moment_of_inertia.py 
# 
# Created:  Dec 2025, M. Clarke  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# package imports 
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Cabin Moment of Inertia
# ----------------------------------------------------------------------------------------------------------------------   
def compute_cabin_moment_of_inertia(cabin,center_of_gravity = np.array([[0,0,0]])):  
    """
    Computes the moment of inertia tensor for the cabin.
    
    Parameters
    ----------
    center_of_gravity : list, optional
        Reference point coordinates for moment calculation, defaults to [[0, 0, 0]]
    
    Returns
    -------
    I : ndarray
        3x3 moment of inertia tensor in kg*m^2
    
    See Also
    --------
    RCAIDE.Library.Methods.weights.vehicle.moments_of_inertia.compute_fuselage_moment_of_inertia
        Implementation of the moment of inertia calculation
    """
    # moment of inertia of arbitrary cabin
    I_cg  = 0  # AIDAN TO UPDATE
    
    # additional MOI due to parallel axis theorm 
    s     = np.array(center_of_gravity) - np.array(cabin.mass_properties.center_of_gravity ) 
    I_par = cabin.mass_properties.mass * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - np.outer(s, s))             
    
    cabin.mass_properties.moments_of_inertia.tensor =  I_cg + I_par
    return  cabin.mass_properties.moments_of_inertia.tensor, cabin.mass_properties.mass