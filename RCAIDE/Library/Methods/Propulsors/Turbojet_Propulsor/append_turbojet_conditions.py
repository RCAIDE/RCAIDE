# RCAIDE/Library/Methods/Propulsors/Turbojet_Propulsor/append_turbojet_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_turbojet_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_turbojet_conditions(turbojet,segment,fuel_line,add_additional_network_equation):  
    ones_row    = segment.state.ones_row                  
    segment.state.conditions.energy[fuel_line.tag][turbojet.tag]                      = Conditions()  
    segment.state.conditions.energy[fuel_line.tag][turbojet.tag].throttle             = 0. * ones_row(1)      
    segment.state.conditions.energy[fuel_line.tag][turbojet.tag].orientation          = 0. * ones_row(1)  
    segment.state.conditions.energy[fuel_line.tag][turbojet.tag].thrust               = 0. * ones_row(3) 
    segment.state.conditions.energy[fuel_line.tag][turbojet.tag].moment               = 0. * ones_row(3) 
    segment.state.conditions.energy[fuel_line.tag][turbojet.tag].power                = 0. * ones_row(1) 
    segment.state.conditions.energy[fuel_line.tag][turbojet.tag].inputs               = Conditions()
    segment.state.conditions.energy[fuel_line.tag][turbojet.tag].outputs              = Conditions() 
    segment.state.conditions.noise[fuel_line.tag][turbojet.tag]                       = Conditions() 
    segment.state.conditions.noise[fuel_line.tag][turbojet.tag].turbojet              = Conditions() 
    segment.state.conditions.noise[fuel_line.tag][turbojet.tag].turbojet.core_nozzle  = Conditions()   
    return 