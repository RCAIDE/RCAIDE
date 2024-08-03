# RCAIDE/Library/Methods/Propulsors/Turboshaft_Propulsor/append_turboshaft_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_turboshaft_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_turboshaft_conditions(turboshaft,segment,fuel_line,add_additional_network_equation):  
    ones_row    = segment.state.ones_row                  
    segment.state.conditions.energy[fuel_line.tag][turboshaft.tag]                        = Conditions()  
    segment.state.conditions.energy[fuel_line.tag][turboshaft.tag].throttle               = 0. * ones_row(1)      
    segment.state.conditions.energy[fuel_line.tag][turboshaft.tag].orientation            = 0. * ones_row(1)   
    segment.state.conditions.energy[fuel_line.tag][turboshaft.tag].power                  = 0. * ones_row(1) 
    segment.state.conditions.energy[fuel_line.tag][turboshaft.tag].inputs                 = Conditions()
    segment.state.conditions.energy[fuel_line.tag][turboshaft.tag].outputs                = Conditions() 
    segment.state.conditions.noise[fuel_line.tag][turboshaft.tag]                         = Conditions() 
    segment.state.conditions.noise[fuel_line.tag][turboshaft.tag].turboshaft              = Conditions() 
    segment.state.conditions.noise[fuel_line.tag][turboshaft.tag].turboshaft.core_nozzle  = Conditions()   
    return 