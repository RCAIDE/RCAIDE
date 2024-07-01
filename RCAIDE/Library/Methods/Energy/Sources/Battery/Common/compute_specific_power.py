## @ingroup Library-Methods-Energy-Sources-Battery-Ragone
# RCAIDE/Library/Methods/Energy/Sources/Battery/Ragone/find_specific_power.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 
 
# ----------------------------------------------------------------------------------------------------------------------
#  find_specific_power
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Sources-Battery-Ragone
def find_specific_power(battery, specific_energy):
    """Determines specific specific power from a ragone curve correlation
    
    Assumptions:
       None
    
    Source:
       Noen
       
    Args:
      battery          (dict): battery data structure [-]
      specific_energy (float): specific energy        [J/kg]     
                
    Returns:
       None 
    """
    
    const_1                 = battery.ragone.const_1
    const_2                 = battery.ragone.const_2
    specific_power          = const_1*10.**(const_2*specific_energy)
    battery.specific_power  = specific_power
    battery.specific_energy = specific_energy
    
    return 