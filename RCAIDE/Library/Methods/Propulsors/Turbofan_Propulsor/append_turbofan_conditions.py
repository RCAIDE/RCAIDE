# RCAIDE/Library/Methods/Propulsors/Turbofan_Propulsor/append_turbofan_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_turbofan_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_turbofan_conditions(turbofan,segment,fuel_line,add_additional_network_equation):  
    ones_row    = segment.state.ones_row                  
    segment.state.conditions.energy[fuel_line.tag][turbofan.tag]                               = Conditions()  
    segment.state.conditions.energy[fuel_line.tag][turbofan.tag].throttle                      = 0. * ones_row(1)      
    segment.state.conditions.energy[fuel_line.tag][turbofan.tag].commanded_thrust_vector_angle = 0. * ones_row(1)  
    segment.state.conditions.energy[fuel_line.tag][turbofan.tag].thrust                        = 0. * ones_row(3) 
    segment.state.conditions.energy[fuel_line.tag][turbofan.tag].power                         = 0. * ones_row(1) 
    segment.state.conditions.energy[fuel_line.tag][turbofan.tag].moment                        = 0. * ones_row(3) 
    segment.state.conditions.energy[fuel_line.tag][turbofan.tag].inputs                        = Conditions()
    segment.state.conditions.energy[fuel_line.tag][turbofan.tag].outputs                       = Conditions() 
    segment.state.conditions.noise[fuel_line.tag][turbofan.tag]                                = Conditions() 
    segment.state.conditions.noise[fuel_line.tag][turbofan.tag].turbofan                       = Conditions() 
    segment.state.conditions.noise[fuel_line.tag][turbofan.tag].turbofan.core_nozzle           = Conditions() 
    segment.state.conditions.noise[fuel_line.tag][turbofan.tag].turbofan.fan_nozzle            = Conditions() 
    segment.state.conditions.noise[fuel_line.tag][turbofan.tag].turbofan.fan                   = Conditions()  
    return 