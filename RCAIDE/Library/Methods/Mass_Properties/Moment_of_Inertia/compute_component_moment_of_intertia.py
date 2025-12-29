# RCAIDE/Library/Methods/Mass_Properties/Moment_of_Intertia/sum_component_moments_of_intertia.py 
# 
# Created:  Jul 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
import RCAIDE
from RCAIDE.Library.Components                                 import Component   

# ----------------------------------------------------------------------------------------------------------------------
#  Recursive MOI
# ----------------------------------------------------------------------------------------------------------------------   
def compute_component_moment_of_intertia(component,vehicle,total_MOI,segment):
    """ Recursively computes the compute moment of inertia all components and subcomponents

    Assumptions:
    None

    Source:
    N/A

    Inputs:
       compoment

    Outputs:
       None
    """      

    if isinstance(component,Component.Container): 
        for key in component.keys():
            item = component[key]        
            compute_component_moment_of_intertia(item,vehicle,total_MOI,segment)
    if isinstance(component,Component):
        component.compute_moments_of_inertia(vehicle)
        update_moment_of_inertia(total_MOI,component,segment) 
        if isinstance(component,RCAIDE.Library.Components.Powertrain.Sources.Fuel_Tanks.Fuel_Tank):
            update_moment_of_inertia(total_MOI,component.fuel,segment) 
        for key in component.keys():
            item = component[key]
            if isinstance(item,Component.Container):
                compute_component_moment_of_intertia(item,vehicle,total_MOI,segment)
        
    return total_MOI
 

def update_moment_of_inertia(total_MOI,C,segment=None):  
    ones_row      = segment.state.ones_row  
    I             = C.mass_properties.moments_of_inertia.tensor
    total_MOI    += I  
    if segment != None:
        segment.state.conditions.weights.components.moments_of_inertia_Ixx[C.tag] = I[0][0]  * ones_row(1) 
        segment.state.conditions.weights.components.moments_of_inertia_Ixy[C.tag] = I[0][1]  * ones_row(1)
        segment.state.conditions.weights.components.moments_of_inertia_Ixz[C.tag] = I[0][2]  * ones_row(1)
        segment.state.conditions.weights.components.moments_of_inertia_Iyx[C.tag] = I[1][0]  * ones_row(1)
        segment.state.conditions.weights.components.moments_of_inertia_Iyy[C.tag] = I[1][1]  * ones_row(1)
        segment.state.conditions.weights.components.moments_of_inertia_Iyz[C.tag] = I[1][2]  * ones_row(1)
        segment.state.conditions.weights.components.moments_of_inertia_Izx[C.tag] = I[2][0]  * ones_row(1)
        segment.state.conditions.weights.components.moments_of_inertia_Izy[C.tag] = I[2][1]  * ones_row(1)
        segment.state.conditions.weights.components.moments_of_inertia_Izz[C.tag] = I[2][2]  * ones_row(1)   
    return total_MOI
