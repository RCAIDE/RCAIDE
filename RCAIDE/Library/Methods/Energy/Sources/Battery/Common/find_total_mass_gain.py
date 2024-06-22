## @ingroup Library-Methods-Energy-Battery-Common
# RCAIDE/Library/Methods/Energy/Sources/Battery/Common/find_total_mass_gain.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Battery-Common
def find_total_mass_gain(battery):
    """finds the total mass of air that the battery 
    accumulates when discharged fully
    
    Assumptions:
    Earth Atmospheric composition
    
    Args:
    battery.pack.maximum_energy [J]
    battery.
      mass_gain_factor [kg/W]
      
    Returns:
      mdot             [kg]
    """ 
    
    mgain=battery.pack.maximum_energy*battery.mass_gain_factor
    
    return mgain