# RCAIDE/Library/Methods/Mass_Properties/Center_of_Gravity/compute_vehicle_center_of_gravity.py 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports      
from RCAIDE.Library.Methods.Mass_Properties.Center_of_Gravity.compute_component_center_of_gravity import compute_component_center_of_gravity 

# package imports 
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
#  Computer Aircraft Center of Gravity
# ----------------------------------------------------------------------------------------------------------------------   
def compute_vehicle_center_of_gravity(vehicle,overwrite_center_of_gravity=True,segment=None,verbose=True): 
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
    if verbose:
        print("\n\n=== COMPONENT CENTER OF GRAVITY BREAKDOWN REPORT ===" )    
        print("Component \t \t \t Mass \t \t C.G. Location [[x,y,z]]" )    
    
    #==========================================================================================
    # Compute the center of gravity of all components  
    #==========================================================================================   
    total_moment = np.array([[0.0,0.0,0.0]])
    total_mass   = np.array([0.0])                
    for key in vehicle.keys():
        item = vehicle[key]  
        total_mass,total_moment = compute_component_center_of_gravity(item,vehicle,total_mass,total_moment ,segment, verbose)    
    
    # print center of gravity 
    CG =  total_moment / total_mass
    if verbose:
        print('\n ***** Aircraft center of gravity ***** ')
        print(CG) 
        mass_percentage = (total_mass[0] / vehicle.mass_properties.takeoff) * 100
        print('Mass used in CG and MOI calculations: ', round(total_mass[0],2))
        print('Mass percentage of TOW used in CG and MOI calculations: ', round(mass_percentage,2), '%')
        
 
    if segment != None:         
        ones_row  = segment.state.ones_row  
        segment.state.conditions.weights.vehicle.global_center_of_gravity = CG * ones_row(1)
     
    # Update CG if flag is true         
    if overwrite_center_of_gravity and (total_mass != 0.0): 
        vehicle.mass_properties.center_of_gravity = CG.tolist()
        
    return vehicle.mass_properties.center_of_gravity, total_moment, total_mass 
