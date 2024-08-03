# RCAIDE/Library/Methods/Propulsors/Electric_Rotor_Propulsor/unpack_electric_rotor_unknowns.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke   

# ---------------------------------------------------------------------------------------------------------------------- 
#  unpack electric rotor network unknowns 
# ----------------------------------------------------------------------------------------------------------------------  

def unpack_electric_rotor_unknowns(propulsor,segment,bus,add_additional_network_equation): 
    bus_results = segment.state.conditions.energy[bus.tag]
    rotor       =  propulsor.rotor 
    if add_additional_network_equation:
        bus_results[propulsor.tag][rotor.tag].power_coefficient = segment.state.unknowns[propulsor.tag  + '_rotor_cp'] 
    return 