## @ingroup Library-Methods-Energy-Sources-Battery-Aluminum_Air
# RCAIDE/Library/Methods/Energy/Sources/Battery/Aluminum_Air/compute_al_air_cell_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  compute_aluminum_mass
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Methods-Energy-Sources-Battery-Aluminum_Air
def compute_aluminum_mass(battery, energy):
    """ Compute Mass of Aluminum battery
    
    Assumtions:
        None
        
    Source:
        None
    
    Args:
        battery  (dict): Battery data structure [-]
        energy  (float): battery energy         [J]
    
    Returns:
        aluminum_mass (float): Al battery mass  [kg]
        
    """
    aluminum_mass = energy*battery.aluminum_mass_factor
    return aluminum_mass 

# ----------------------------------------------------------------------------------------------------------------------
#  compute_water_mass
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Methods-Energy-Sources-Battery-Aluminum_Air
def compute_water_mass(battery, energy):
    """ Compute water mass of Aluminum battery
    
    Assumtions:
        None
        
    Source:
        None
    
    Args:
        battery  (dict): Battery data structure [-]
        energy  (float): battery energy         [J]
    
    Returns:
        aluminum_mass (float): Al battery mass  [kg] 
    """
    water_mass = energy*battery.water_mass_gain_factor
    return water_mass
