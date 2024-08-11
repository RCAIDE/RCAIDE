# RCAIDE/Library/Methods/Propulsors/Electric_Rotor_Propulsor/unpack_electric_rotor_unknowns.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke   

# ---------------------------------------------------------------------------------------------------------------------- 
#  unpack electric rotor network unknowns 
# ----------------------------------------------------------------------------------------------------------------------  

def unpack_electric_rotor_unknowns(propulsor,reference_propulsor,segment,bus): 
    bus_results = segment.state.conditions.energy[bus.tag]
    rotor       =  propulsor.rotor  
    bus_results[propulsor.tag][rotor.tag].power_coefficient = segment.state.unknowns[reference_propulsor.tag  + '_rotor_cp'] 
    return 