# RCAIDE/Library/Methods/Mass_Properties/Moment_of_Inertia/compute_fuselage_integral_tank_moment_of_inertia.py 
# 
# Created:  Jan 2026, M. Clarke  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE 

# package imports 
import numpy as np  
# ----------------------------------------------------------------------------------------------------------------------
#  Compute Wing Moment of Inertia
# ----------------------------------------------------------------------------------------------------------------------  
def compute_fuselage_integral_tank_moment_of_inertia(fuel_tank,fuselage, center_of_gravity = [[0, 0, 0]]):

    # intialize matrices 
    I_global_fuel        = np.zeros((3, 3))
    I_local_fuel_non_dim = np.zeros((3, 3))
    I_global_tank        = np.zeros((3, 3))
    I_local_tank_non_dim = np.zeros((3, 3))    
    
    # ADD FUNCTION
    
    
    # Store moment of inertia tensors of tank and fuel 
    fuel_tank.fuel.mass_properties.moments_of_inertia.tensor                 = I_global_fuel
    fuel_tank.fuel.mass_properties.moments_of_inertia.non_dimensional_tensor = I_local_fuel_non_dim
    fuel_tank.mass_properties.moments_of_inertia.tensor                      = I_global_tank
    fuel_tank.mass_properties.moments_of_inertia.non_dimensional_tensor      = I_local_tank_non_dim     
    return 

 