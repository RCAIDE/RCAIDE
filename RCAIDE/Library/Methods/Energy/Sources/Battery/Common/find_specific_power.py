## @ingroup Library-Methods-Energy-Battery-Ragone
# RCAIDE/Library/Methods/Energy/Sources/Battery/Ragone/find_specific_power.py
# 
# 
# Created:  Jul 2023, M. Clarke 
 
# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Battery-Ragone
def find_specific_power(battery, specific_energy):
    """determines specific specific power from a ragone curve correlation
    Assumptions:
    None
    
    Args:
    battery.
      specific_energy [J/kg]               
      ragone.
        constant_1    [W/kg]
        constant_2    [J/kg]
                
    Returns:
    battery.
      specific_power  [W/kg]   
    
    
    
    """
    
    const_1                 = battery.ragone.const_1
    const_2                 = battery.ragone.const_2
    specific_power          = const_1*10.**(const_2*specific_energy)
    battery.specific_power  = specific_power
    battery.specific_energy = specific_energy