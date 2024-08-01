# RCAIDE/Library/Methods/Energy/Auxillary_Systems/auxillary_systems_power.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# compute_payload_power_consumption
# ----------------------------------------------------------------------------------------------------------------------
def compute_payload_power_consumption(payload):
    """This gives the power draw from a payload.

    Assumptions:
        None

    Source:
        None

    Args:
        payload.power_draw (float): power consumed by payload [Watts] 

    Returns:
        payload.outputs.power_draw (float): power consumed by payload [Watts] 
    """          
    payload.inputs.power = payload.power_draw
    
    return payload.power_draw
 
# ----------------------------------------------------------------------------------------------------------------------
# compute_avionics_power_consumption
# ----------------------------------------------------------------------------------------------------------------------    
def  compute_avionics_power_consumption(avionics):
    """This gives the power draw from avionics.

    Assumptions:
        None

    Source:
        None

    Args: 
        avionics.power_draw (float): power consumed by avionics [Watts]     

    Returns:
        avionics.outputs.power_draw  (float): power consumed by avionics [Watts] 
    """                 
    avionics.inputs.power =  avionics.power_draw
    
    return  avionics.power_draw