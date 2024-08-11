# RCAIDE/Library/Methods/Propulsors/Electric_Rotor_Propulsor/pack_ice_propeller_residuals.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke   

# ---------------------------------------------------------------------------------------------------------------------- 
#  pack ice propeller residuals
# ----------------------------------------------------------------------------------------------------------------------  

def pack_ice_propeller_residuals(propulsor,segment,fuel_line): 
    fuel_line_results       = segment.state.conditions.energy[fuel_line.tag]  
    q_engine   = fuel_line_results[propulsor.tag].engine.torque
    q_prop     = fuel_line_results[propulsor.tag].rotor.torque 
    segment.state.residuals.network[ fuel_line.tag + '_' + propulsor.tag + '_rotor_engine_torque'] = q_engine - q_prop 
    return 
