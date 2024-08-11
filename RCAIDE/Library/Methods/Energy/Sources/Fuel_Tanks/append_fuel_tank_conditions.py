## @ingroup Methods-Energy-Sources-Battery 
# RCAIDE/Methods/Energy/Sources/Fuel_Tanks/append_fuel_tank_conditions.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Framework.Mission.Common     import   Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Sources-Battery 
def append_fuel_tank_conditions(fuel_tank,segment,fuel_line): 
    ones_row    = segment.state.ones_row                 
    segment.state.conditions.energy[fuel_line.tag][fuel_tank.tag]                 = Conditions()  
    segment.state.conditions.energy[fuel_line.tag][fuel_tank.tag].mass_flow_rate  = ones_row(1)  
    segment.state.conditions.energy[fuel_line.tag][fuel_tank.tag].mass            = ones_row(1)
    
    return 
