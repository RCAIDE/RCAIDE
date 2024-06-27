## @ingroup Library-Methods-Thermal_Management-Batteries-Heat_Exchanger_Systems-No_Heat_Exchanger 
# RCAIDE/Library/Methods/Thermal_Management/Batteries/Heat_Exchanger_Systems/No_Heat_Exchanger/no_heat_exchanger_model.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from RCAIDE.Framework.Core import Data

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Net Convected Heat 
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Thermal_Management-Batteries-Atmospheric_Air_Convection_Cooling 
def no_heat_exchanger_model(HEX,HAS_outputs,state,dt,i):
    '''Computes no heat removed by heat exchanger system into the environment

    Assumptions:
        None
        
    Source:
       None
        
    Args:
       None
    
    Returns:
       None
    ''' 
     
    HEX_outputs            = Data(total_heat_removed   = 0)    
    return HEX_outputs 