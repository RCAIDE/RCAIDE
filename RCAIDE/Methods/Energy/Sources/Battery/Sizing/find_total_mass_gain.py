## @ingroup Methods-Energy-Sources-Battery-Sizing
# RCAIDE/Methods/Energy/Sources/Battery/Sizing/find_total_mass_gain.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Sources-Battery-Sizing
def find_total_mass_gain(battery):
    """finds the total mass of air that the battery 
    accumulates when discharged fully
    
    Assumptions:
    Earth Atmospheric composition
    
    Inputs:
    battery.pack.maximum_energy [J]
    battery.
      mass_gain_factor [kg/W]
      
    Outputs:
      mdot             [kg]
    """ 
    
    mgain=battery.pack.maximum_energy*battery.mass_gain_factor
    
    return mgain