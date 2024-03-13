## @ingroup Library-Methods-Energy-Battery-Common
# RCAIDE/Library/Methods/Energy/Sources/Battery/Common/find_mass_gain_rate.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Battery-Common
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