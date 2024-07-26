# RCAIDE/Library/Methods/Propulsors/Converters/Combustor/append_motor_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_motor_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_motor_conditions(motor,segment,propulsor_conditions): 
    propulsor_conditions[motor.tag]         = Conditions()
    propulsor_conditions[motor.tag].inputs  = Conditions()
    propulsor_conditions[motor.tag].outputs = Conditions()
    return 
