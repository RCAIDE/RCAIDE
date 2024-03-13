## @ingroup Methods-Energy-Sources-Battery-Common
# RCAIDE/Library/Methods/Energy/Sources/Battery/Common/initialize_from_energy_and_power.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from RCAIDE.Library.Methods.Utilities import soft_max

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Sources-Battery-Common
def initialize_from_energy_and_power(battery, energy, power, max='hard'):
    """
    Uses a soft_max function to calculate the batter mass, maximum energy, and maximum power
    from the energy and power requirements, as well as the specific energy and specific power
    
    Assumptions:
    None
    
    Inputs:
    energy            [J]
    power             [W]
    battery.
      specific_energy [J/kg]               
      specific_power  [W/kg]
    
    Outputs:
     battery.
       maximum_energy
       maximum_power
       mass_properties.
        mass
    
    
    """
    
    energy_mass = energy/battery.specific_energy
    power_mass  = power/battery.specific_power
    
    if max=='soft': #use softmax function (makes it differentiable)
        mass=soft_max(energy_mass,power_mass)
        
    else:
        mass=np.maximum(energy_mass, power_mass)

    battery.mass_properties.mass = mass
    battery.pack.maximum_energy  = battery.specific_energy*mass
    battery.pack.maximum_power       = battery.specific_power*mass
    
    return 