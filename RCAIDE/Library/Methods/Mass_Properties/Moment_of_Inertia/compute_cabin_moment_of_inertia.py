# RCAIDE/Library/Methods/Mass_Properties/Moment_of_Inertia/compute_cabin_moment_of_inertia.py 
# 
# Created:  Dec 2025, M. Clarke  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# package imports 
import numpy as np 
import RCAIDE
from RCAIDE.Library.Methods.Mass_Properties.Moment_of_Inertia.compute_cuboid_moment_of_inertia import compute_cuboid_moment_of_inertia

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Cabin Moment of Inertia
# ----------------------------------------------------------------------------------------------------------------------   
def compute_cabin_moment_of_inertia(cabin,center_of_gravity = np.array([[0,0,0]])):  
    '''  
 
    N/A
    '''
    # SAI& AIDAN : UPDATE WITH PARALLEL AXIS THEOREM -- THIS IS PARTIALLY DONE AND NEEDS TO BE CHECKED, 12/29/2025
    s                = cabin.center_of_gravity - center_of_gravity # Vector for the parallel axis theorem
    
    # UNSURE IF CABIN MOI WILL HAVE BEEN PROPERLY UPDATED 
    # I_cabin = cabin.mass_properties.moments_of_inertia.tensor
    cabin.mass_properties.moments_of_inertia.tensor, _ =  compute_cuboid_moment_of_inertia(cabin, cabin.length, cabin.width, cabin.height)

    cabin.mass_properties.moments_of_inertia.tensor += cabin.mass_properties.mass * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - np.outer(s, s))             

    return  cabin.mass_properties.moments_of_inertia.tensor, cabin.mass_properties.mass