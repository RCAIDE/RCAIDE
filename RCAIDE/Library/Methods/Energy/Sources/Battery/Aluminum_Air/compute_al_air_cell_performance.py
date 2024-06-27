## @ingroup Methods-Energy-Sources-Battery-Aluminum_Air
# RCAIDE/Methods/Energy/Sources/Battery/Aluminum_Air/compute_al_air_cell_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  compute_al_air_cell_performance
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Methods-Energy-Sources-Battery-Aluminum_Air
def find_aluminum_mass(battery, energy):
    aluminum_mass = energy*battery.aluminum_mass_factor
    return aluminum_mass 

def find_water_mass(battery, energy):
    water_mass = energy*battery.water_mass_gain_factor
    return water_mass
