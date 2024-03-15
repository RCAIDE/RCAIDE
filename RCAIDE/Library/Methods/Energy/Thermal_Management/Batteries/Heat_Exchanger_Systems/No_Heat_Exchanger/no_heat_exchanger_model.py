## @ingroup Library-Methods-Thermal_Management-Batteries-Heat_Exchanger_Systems-No_Heat_Exchanger 
# RCAIDE/Library/Methods/Thermal_Management/Batteries/Heat_Exchanger_Systems/No_Heat_Exchanger/no_heat_exchanger_model.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# 
# Created:  Jul 2023, M. Clarke 

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
        
    Inputs:   
    
    Outputs: 

    Properties Used:
    None 
    ''' 
     
    HEX_outputs            = Data(total_heat_removed   = 0)    
    return HEX_outputs 


def _no_heat_exchanger_model(State, Settings, System):
	'''
	Framework version of no_heat_exchanger_model.
	Wraps no_heat_exchanger_model with State, Settings, System pack/unpack.
	Please see no_heat_exchanger_model documentation for more details.
	'''

	#TODO: HEX         = [Replace With State, Settings, or System Attribute]
	#TODO: HAS_outputs = [Replace With State, Settings, or System Attribute]
	#TODO: state       = [Replace With State, Settings, or System Attribute]
	#TODO: dt          = [Replace With State, Settings, or System Attribute]
	#TODO: i           = [Replace With State, Settings, or System Attribute]

	results = no_heat_exchanger_model('HEX', 'HAS_outputs', 'state', 'dt', 'i')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System