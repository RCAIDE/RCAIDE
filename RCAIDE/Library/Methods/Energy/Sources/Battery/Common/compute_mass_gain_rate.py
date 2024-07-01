## @ingroup Library-Methods-Energy-Sources-Battery-Common
# RCAIDE/Library/Methods/Energy/Sources/Battery/Common/compute_mass_gain_rate.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
# compute_mass_gain_rate
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Sources-Battery-Common
def compute_mass_gain_rate(battery,power):
    """Compute the mass gain rate of the battery from the ambient air
    
    Assumptions:
        None 
    
    Source:
       None
       
    Args:
       power                    (float): power            [W]
       battery.mass_gain_factor (float): mass_gain_factor [kg/W]
      
    Returns:
       mdot (float): weight gain rate [kg/s]
    """
    
    # weight gain rate of battery (positive means mass loss)
    mdot = - power * battery.mass_gain_factor   
                
    return mdot