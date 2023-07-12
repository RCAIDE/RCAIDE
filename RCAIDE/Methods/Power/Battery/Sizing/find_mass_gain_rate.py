# RCAIDE/Methods/Power/Battery/Sizing/find_mass_gain_rate.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Power-Battery-Variable_Mass 
def find_mass_gain_rate(battery,power):
    """finds the mass gain rate of the battery from the ambient air
    Assumptions:
    Earth Atmospheric composition
    
    Inputs:
    power              [W]
    battery.
      mass_gain_factor [kg/W]
      
    Outputs:
      mdot             [kg/s]
    """
    
    #weight gain of battery (positive means mass loss)
    mdot = -(power) *(battery.mass_gain_factor)  
                
    return mdot