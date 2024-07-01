## @ingroup Library-Methods-Energy-Sources-Battery-Common
# RCAIDE/Library/Methods/Energy/Sources/Battery/Common/size_pack_from_energy_and_power.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from RCAIDE.Library.Methods.Utilities import soft_max

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  size_pack_from_energy_and_power
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Sources-Battery-Common
def size_pack_from_energy_and_power(battery, energy, power,pack_markup_factor = 1.42, max='hard'):
    """ Uses a soft_max function to calculate the batter mass, maximum energy, and maximum power
    from the energy and power requirements, as well as the specific energy and specific power
    
    Assumptions:
    1) Total battery pack mass contains build-up factor (1.42) for battery casing,
       internal wires, thermal management system and battery management system 
       Factor computed using information of battery properties for X-57 Maxwell
       Aircraft
    
    Source:
        None 

    Args:
       battery              (dict): battery data structure [-]
       energy              (float): battery energy         [unitless]
       power               (float): battery power          [unitless]
       pack_markup_factor (float): pack mark up factor     [unitless]


    Returns:
        None  
    """ 
    
    energy_mass = energy/battery.specific_energy
    power_mass  = power/battery.specific_power
    
    if max=='soft': #use softmax function (makes it differentiable)
        mass=soft_max(energy_mass,power_mass)
        
    else:
        mass=np.maximum(energy_mass, power_mass)

    battery.mass_properties.mass = mass * pack_markup_factor
    battery.pack.maximum_energy  = battery.specific_energy*mass
    battery.pack.maximum_power   = battery.specific_power*mass
    battery.pack.specific_energy = battery.pack.maximum_energy / battery.mass_properties.mass
    
    return 