# RCAIDE/Library/Methods/Propulsors/Converters/Rotor/append_rotor_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_motor_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_rotor_conditions(rotor,segment,energy_conditions,noise_conditions): 
    ones_row    = segment.state.ones_row 
    energy_conditions[rotor.tag]                   = Conditions()
    energy_conditions[rotor.tag].inputs            = Conditions()     
    energy_conditions[rotor.tag].orientation       = 0. * ones_row(3)  
    energy_conditions[rotor.tag].pitch_command     = 0. * ones_row(1)
    energy_conditions[rotor.tag].torque            = 0. * ones_row(1)
    energy_conditions[rotor.tag].thrust            = 0. * ones_row(1)
    energy_conditions[rotor.tag].rpm               = 0. * ones_row(1)
    energy_conditions[rotor.tag].omega             = 0. * ones_row(1)
    energy_conditions[rotor.tag].disc_loading      = 0. * ones_row(1)                 
    energy_conditions[rotor.tag].power_loading     = 0. * ones_row(1)
    energy_conditions[rotor.tag].tip_mach          = 0. * ones_row(1)
    energy_conditions[rotor.tag].efficiency        = 0. * ones_row(1)   
    energy_conditions[rotor.tag].power_coefficient = 0. * ones_row(1) 
    noise_conditions[rotor.tag]                    = Conditions() 
    return 
