# RCAIDE/Library/Methods/Thermal_Management/Batteries/Air_Cooled/append_air_cooling_conditions.py
# 
# Created:  Aug 2024, S. Shekar

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_turbofan_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_air_cooled_conditions(air_cooled,segment,coolant_line,add_additional_network_equation):
    ones_row                                                                                        = segment.state.ones_row                  
    segment.state.conditions.energy[coolant_line.tag][air_cooled.tag]                               = Conditions()
    segment.state.conditions.energy[coolant_line.tag][air_cooled.tag].effectiveness                 = 0. * ones_row(1)
    segment.state.conditions.energy[coolant_line.tag][air_cooled.tag].total_heat_removed            = 0. * ones_row(1)
    return

def append_air_cooled_segment_conditions(air_cooled, segment,coolant_line, conditions):
    
    air_cooled_conditions = conditions[coolant_line.tag][air_cooled.tag]
    if segment.state.initials:  
        air_cooled_initials                            = segment.state.initials.conditions.energy[coolant_line.tag][air_cooled.tag]
        air_cooled_conditions.effectiveness[:,0]       = air_cooled_initials.effectiveness[-1,0]     
        air_cooled_conditions.total_heat_removed[:,0]  = air_cooled_initials.total_heat_removed[-1,0]   
        
    
    return

    
    

    
    