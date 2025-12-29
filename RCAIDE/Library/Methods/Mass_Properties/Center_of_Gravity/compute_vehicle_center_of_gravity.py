# RCAIDE/Library/Methods/Mass_Properties/Center_of_Gravity/compute_vehicle_center_of_gravity.py 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports   
import RCAIDE 
from RCAIDE.Library.Components import Component   
from RCAIDE.Library.Methods.Mass_Properties.Center_of_Gravity.compute_component_center_of_gravity import compute_component_center_of_gravity 

# package imports 
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
#  Computer Aircraft Center of Gravity
# ----------------------------------------------------------------------------------------------------------------------   
def compute_vehicle_center_of_gravity(vehicle,update_center_of_gravity=True, segment=None): 
    ''' Computes the moment of inertia of aircraft 
    
    Source:
    Simplified Mass and Inertial Estimates for Aircraft with Components of Constant Density
    Moulton, B. C., and Hunsaker, D. F., “Simplified Mass and Inertial Estimates for Aircraft with Components 
    of Constant Density,” AIAA SCITECH 2023 Forum, January 2023, AIAA-2023-2432 DOI: 10.2514/
    6.2023-2432
    
    
    Assumtions:
    Assumes simplified shapes 
    
    Inputs:
    vehicle           - vehicle data structure           [m]
    
    Outputs:
    I                 - mass moment of inertia matrix    [kg-m^2]
    
    ''' 

    # unpack 
    ones_row      = segment.state.ones_row
    
    #==========================================================================================
    # Compute the center of gravity of all components  
    #==========================================================================================   
    total_moment = np.array([[0.0,0.0,0.0]])
    total_mass   = np.array([0.0])                
    for key in vehicle.keys():
        item = vehicle[key]  
        total_mass,total_moment = compute_component_center_of_gravity(item,vehicle,total_mass,total_moment ,segment)    
    
    # compute center of gravity 
    CG =  total_moment / total_mass

    # if simulations is part of a mission, store MOI in results vector 
    if segment != None:        
        # store aircraft MOI
        segment.state.conditions.weights.vehicle.center_of_gravity = CG * ones_row(1) 
     
    # Update CG if flag is true         
    if update_center_of_gravity and total_mass != 0.0: 
        vehicle.mass_properties.center_of_gravity = CG.tolist()
        
    return vehicle.mass_properties.center_of_gravity, total_moment, total_mass 
