## @ingroup Library-Methods-Energy-Sources-Battery-Ragone
# RCAIDE/Library/Methods/Energy/Sources/Battery/Ragone/compute_ragone_properties.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
from .  import size_pack_from_energy_and_power
from .  import compute_specific_power 

# ----------------------------------------------------------------------------------------------------------------------
#  compute_ragone_properties
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Sources-Battery-Ragone
def compute_ragone_properties(specific_energy, battery, energy, power):
    """determines mass of a battery based on the specific energy, energy required, and power required,
    works by calling find_specific_power and initialize_from_energy_and_power
         
    Assumptions:
        None
        
    Source:
        None 
    
    Args:
        specific_energy (float):specific_energy        [J/kg]
        battery          (dict): battery data struture [-]      
        energy          (float):energy                 [J]
        power           (float):power                  [W]
                
    Returns:
        battery.mass_properties.mass      [kg]     
    """  
    
    compute_specific_power(battery, specific_energy)
    size_pack_from_energy_and_power(battery, energy, power)
    
    return battery.mass_properties.mass 