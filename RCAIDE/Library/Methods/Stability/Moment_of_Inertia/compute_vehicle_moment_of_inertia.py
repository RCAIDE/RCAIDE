## @ingroup Methods-Stability-compoment_I
# RCAIDE/Methods/Stability/compoment_I/compute_compoments_moments_of_intertia.py 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from Legacy.trunk.S.Components import Physical_Component 
from RCAIDE.Library.Components import Component 
from RCAIDE.Library.Methods.Stability.Common import * 
from .compute_component_moments_of_inertia import compute_component_moments_of_inertia
import numpy as np 


# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Moment of Inertia of Cuboid  
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Stability-compoment_I 
def compute_vehicle_moment_of_inertia(vehicle):
    
    """  
    """   
    compute_component_moments_of_inertia(vehicle)
    
    CG = vehicle.mass_properties.center_of_gravity
    total_I = np.array([[0.0,0.0,0.0]]) 

    for key in vehicle.keys():
        item = vehicle[key]
        if isinstance(item,Physical_Component.Container) or isinstance(item,Component.Container):
            total_I      += sum_moment_of_intertia(item, vehicle_center_of_gravity = CG)  
    for network in vehicle.networks:
        for net_key in network.keys():
            net_item = network[net_key] 
            if isinstance(net_item,Energy_Component.Container): 
                total_I      += sum_moment_of_intertia(net_item, vehicle_center_of_gravity = CG)   
        for bus in network.busses: 
            total_I      += sum_moment_of_intertia(bus, vehicle_center_of_gravity = CG)  
        for fuel_line in network.fuel_lines: 
            total_I      += sum_moment_of_intertia(fuel_line, vehicle_center_of_gravity = CG)   
            
    vehicle.mass_properties.moments_of_inertia.center = total_I
            
    return  



   

