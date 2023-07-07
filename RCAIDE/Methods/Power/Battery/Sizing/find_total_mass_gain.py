# RCAIDE/Methods/Power/Battery/Sizing/find_total_mass_gain.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Power-Battery-Sizing
def find_total_mass_gain(battery):
    """finds the total mass of air that the battery 
    accumulates when discharged fully
    
    Assumptions:
    Earth Atmospheric composition
    
    Inputs:
    battery.pack.max_energy [J]
    battery.
      mass_gain_factor [kg/W]
      
    Outputs:
      mdot             [kg]
    """ 
    
    mgain=battery.pack.max_energy*battery.mass_gain_factor
    
    return mgain