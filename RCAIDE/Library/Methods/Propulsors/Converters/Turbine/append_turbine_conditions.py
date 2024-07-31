# RCAIDE/Library/Methods/Propulsors/Converters/turbine/append_turbine_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  
# ----------------------------------------------------------------------------------------------------------------------    
def append_turbine_conditions(turbine,segment,propulsor_conditions): 
    propulsor_conditions[turbine.tag]            = Conditions()
    propulsor_conditions[turbine.tag].inputs     = Conditions()
    propulsor_conditions[turbine.tag].outputs    = Conditions()
    return 