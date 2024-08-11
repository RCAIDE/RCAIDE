# RCAIDE/Library/Methods/Propulsors/ICE_Propulsor/append_ice_propeller_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

from RCAIDE.Framework.Mission.Common     import   Conditions
from RCAIDE.Framework.Core               import Units

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_ice_propeller_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_ice_propeller_conditions(propulsor,segment,fuel_line,add_additional_network_equation):  
    ones_row    = segment.state.ones_row                  
    segment.state.conditions.energy[fuel_line.tag][propulsor.tag]                      = Conditions()  
    segment.state.conditions.energy[fuel_line.tag][propulsor.tag].throttle             = 0. * ones_row(1)      
    segment.state.conditions.energy[fuel_line.tag][propulsor.tag].orientation          = 0. * ones_row(1)  
    segment.state.conditions.energy[fuel_line.tag][propulsor.tag].thrust               = 0. * ones_row(3) 
    segment.state.conditions.energy[fuel_line.tag][propulsor.tag].power                = 0. * ones_row(1) 
    segment.state.conditions.energy[fuel_line.tag][propulsor.tag].moment               = 0. * ones_row(3) 
    segment.state.conditions.energy[fuel_line.tag][propulsor.tag].inputs               = Conditions()
    segment.state.conditions.energy[fuel_line.tag][propulsor.tag].outputs              = Conditions() 
    segment.state.conditions.noise[fuel_line.tag][propulsor.tag]                       = Conditions() 
    segment.state.conditions.noise[fuel_line.tag][propulsor.tag].rotor                 = Conditions()
     
    if add_additional_network_equation: 
        propeller  = propulsor.propeller 
        segment.state.unknowns[propulsor.tag  + '_propeller_rpm'] = ones_row(1) * float(propeller.cruise.design_angular_velocity) /Units.rpm   
        segment.state.residuals.network[ fuel_line.tag + '_' + propulsor.tag + '_rotor_engine_torque'] = 0. * ones_row(1)
                
    return 