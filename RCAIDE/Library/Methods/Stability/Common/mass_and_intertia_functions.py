## @ingroup Methods-Stability-Common
# RCAIDE/Methods/Stability/Common/mass_and_intertia_functions.py 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports   
from RCAIDE.Library.Components         import Component  

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Recursive Moment
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Stability-Common 
def sum_moment(component):
    """ 
    """   
    total_moment = np.array([[0.0,0.0,0.0]])
    total_mass   = 0
    for key,Comp in component.items():
        if  isinstance(Comp,Component.Container):
            Moment, Mass  = sum_moment(Comp)  
            total_moment += Moment
            total_mass   += Mass
        elif isinstance(Comp,Component): 
            global_cg_loc = Comp.mass_properties.center_of_gravity + Comp.origin 
            total_moment += Comp.mass_properties.mass*global_cg_loc 
            total_mass   += Comp.mass_properties.mass     
            
    return total_moment , total_mass

# ----------------------------------------------------------------------------------------------------------------------
#  Recursive Moment of Intertia 
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Stability-Common 
def sum_moment_of_intertia(component, vehicle_center_of_gravity = None):

    total_I = np.array([[0.0,0.0,0.0]]) 
    for key,Comp in component.items():
        if  isinstance(Comp,Component.Container):
            total_I += sum_moment_of_intertia(Comp,vehicle_center_of_gravity )   
        elif isinstance(Comp,Component):   
            global_cg_loc = Comp.mass_properties.center_of_gravity + Comp.origin 
            total_I += Comp.mass_properties.moments_of_inertia.center + Comp.mass_properties.mass*((vehicle_center_of_gravity - global_cg_loc)**2)
            
    return total_I
 

