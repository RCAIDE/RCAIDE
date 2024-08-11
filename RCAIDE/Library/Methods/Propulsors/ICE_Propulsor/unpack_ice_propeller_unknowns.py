# RCAIDE/Library/Methods/Propulsors/Electric_Rotor_Propulsor/unpack_ice_propeller_unknowns.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke   

# ---------------------------------------------------------------------------------------------------------------------- 
#  unpack ice propeller network unknowns 
# ----------------------------------------------------------------------------------------------------------------------  

def unpack_ice_propeller_unknowns(propulsor,reference_propulsor,segment,fuel_line): 
    fuel_line_results = segment.state.conditions.energy[fuel_line.tag]  
    engine            = propulsor.engine 
    fuel_line_results[propulsor.tag][engine.tag].rpm = segment.state.unknowns[reference_propulsor.tag + '_propeller_rpm'] 
    return 