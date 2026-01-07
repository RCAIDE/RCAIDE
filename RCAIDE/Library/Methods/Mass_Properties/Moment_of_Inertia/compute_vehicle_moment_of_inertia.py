# RCAIDE/Library/Methods/Mass_Properties/Moment_of_Inertia/compute_vehicle_moment_of_inertia.py 
# 
# Created:  September 2024, A. Molloy

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Library.Methods.Mass_Properties.Moment_of_Inertia.compute_component_moment_of_intertia import compute_component_moment_of_intertia

# python imports
import numpy as  np
# ------------------------------------------------------------------        
#  Component moments of inertia (MOI) tensors
# ------------------------------------------------------------------  
def compute_vehicle_moment_of_inertia(vehicle, update_moment_of_inertia=True, segment = None,verbose=True): 
    ''' sums the moments of inertia of each component in the aircraft. Components summed: fuselages,
    wings (main, horizontal, tail + others), turbofan engines, batteries, motors, batteries, fuel tanks

    Assumptions:
    - All other components than those listed are insignificant

    Source:
 
    Inputs:
    - vehicle
    - Center of gravity

    Outputs:
    - Total aircraft moment of inertia tensor

    Properties Used:
    N/A
    '''    

    # unpack 
    ones_row      = segment.state.ones_row

    if verbose:
        print("\n\n=== COMPONENT MOMENT OF INTERTIA BREAKDOWN REPORT ===" )    
        print("Component \t \t Ixx \t \t Iyy  \t \t Izz" )        
     
    # Compute the moment of intertia of all components   
    total_MOI    = np.zeros((3, 3))               
    for key in vehicle.keys():
        item       = vehicle[key]  
        total_MOI  = compute_component_moment_of_intertia(item,vehicle,total_MOI ,segment)
    
    # if simulations is part of a mission, store MOI in results vector 
    if segment != None:        
        # store aircraft MOI
        segment.state.conditions.weights.vehicle.moments_of_inertia = total_MOI * ones_row(1) 
    
    # Update MOI if flag is true  
    vehicle.mass_properties.moments_of_inertia.tensor = total_MOI 
        
    return total_MOI 