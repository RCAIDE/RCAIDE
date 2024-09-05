# RCAIDE/Library/Methods/Thermal_Management/Batteries/Air_Cooled/append_air_cooling_conditions.py
# 
# Created:  Aug 2024, S. Shekar

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_turbofan_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_wavy_channel_conditions(wavy_channel,segment,coolant_line,add_additional_network_equation):
     ones_row                                                                                        = segment.state.ones_row
     segment.state.conditions.energy[coolant_line.tag][wavy_channel.tag]                            = Conditions()
     segment.state.conditions.energy[coolant_line.tag][wavy_channel.tag].inlet_coolant_pressure     = 0 * ones_row(1) 
     segment.state.conditions.energy[coolant_line.tag][wavy_channel.tag].heat_removed               = 0 * ones_row(1) 
     segment.state.conditions.energy[coolant_line.tag][wavy_channel.tag].inlet_coolant_temperature  = 0 * ones_row(1)   
     segment.state.conditions.energy[coolant_line.tag][wavy_channel.tag].outlet_coolant_temperature = 0 * ones_row(1) 
     segment.state.conditions.energy[coolant_line.tag][wavy_channel.tag].coolant_mass_flow_rate     = 0 * ones_row(1)  
     segment.state.conditions.energy[coolant_line.tag][wavy_channel.tag].effectiveness              = 0 * ones_row(1)
     segment.state.conditions.energy[coolant_line.tag][wavy_channel.tag].power                      = 0 * ones_row(1)
     
     return