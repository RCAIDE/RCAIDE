## @ingroup Library-Methods-Energy-Sources-Battery-Common
# RCAIDE/Library/Methods/Energy/Sources/Battery/Common/compute_total_mass_gain.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  compute_total_mass_gain
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Sources-Battery-Common
def compute_total_mass_gain(battery):
    """finds the total mass of air that the battery accumulates when discharged fully
    
    Assumptions:
        None
        
    Source:
        None 
    
    Args:
        battery          (dict): battery data struture [-]    
      
    Returns:
      mgain (float): mass gain [kg]
    """  
    mgain = battery.pack.maximum_energy*battery.mass_gain_factor
    
    return mgain