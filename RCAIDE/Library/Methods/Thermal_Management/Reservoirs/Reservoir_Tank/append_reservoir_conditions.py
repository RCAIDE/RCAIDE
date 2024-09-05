# RCAIDE/Library/Methods/Thermal_Management/Batteries/Air_Cooled/append_air_cooling_conditions.py
# 
# Created:  Aug 2024, S. Shekar

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_turbofan_conditions
# ----
def append_reservoir_conditions(reservoir,segment,coolant_line,add_additional_network_equation):
    
    ones_row                                                                                         = segment.state.ones_row
    segment.state.conditions.energy[coolant_line.tag][reservoir.tag]                                 = Conditions()
    segment.state.conditions.energy[coolant_line.tag][reservoir.tag].coolant_temperature             = 0 * ones_row(1)
    return