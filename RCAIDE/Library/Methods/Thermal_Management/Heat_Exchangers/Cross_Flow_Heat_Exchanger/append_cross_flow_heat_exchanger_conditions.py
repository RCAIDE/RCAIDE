# RCAIDE/Library/Methods/Thermal_Management/Batteries/Air_Cooled/append_air_cooling_conditions.py
# 
# Created:  Aug 2024, S. Shekar

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_turbofan_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_cross_flow_heat_exchanger_conditions(cross_flow_hex,segment,coolant_line,add_additional_network_equation):
    ones_row                                                                                         = segment.state.ones_row
    segment.state.conditions.energy[coolant_line.tag][cross_flow_hex.tag]                            = Conditions()
    segment.state.conditions.energy[coolant_line.tag][cross_flow_hex.tag].coolant_mass_flow_rate     = 0 * ones_row(1)  
    segment.state.conditions.energy[coolant_line.tag][cross_flow_hex.tag].power                      = 0 * ones_row(1)  
    segment.state.conditions.energy[coolant_line.tag][cross_flow_hex.tag].inlet_air_temperature      = 0 * ones_row(1) 
    segment.state.conditions.energy[coolant_line.tag][cross_flow_hex.tag].outlet_coolant_temperature = 0 * ones_row(1) 
    segment.state.conditions.energy[coolant_line.tag][cross_flow_hex.tag].air_mass_flow_rate         = 0 * ones_row(1) 
    segment.state.conditions.energy[coolant_line.tag][cross_flow_hex.tag].air_inlet_pressure         = 0 * ones_row(1) 
    segment.state.conditions.energy[coolant_line.tag][cross_flow_hex.tag].coolant_inlet_pressure     = 0 * ones_row(1) 
    segment.state.conditions.energy[coolant_line.tag][cross_flow_hex.tag].pressure_diff_air          = 0 * ones_row(1)
    segment.state.conditions.energy[coolant_line.tag][cross_flow_hex.tag].effectiveness_HEX          = 0 * ones_row(1)
    
    return
    