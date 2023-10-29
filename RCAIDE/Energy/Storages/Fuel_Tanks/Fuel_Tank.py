## @ingroup Energy-Storages-Fuel_Tanks 
# RCAIDE/Energy/Storages/Fuel_Tanks/Fuel_Tanks.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Energy.Energy_Component    import Energy_Component   

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Tank
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Energy-Storages-Fuel_Tanks 
class Fuel_Tank(Energy_Component):
    """
    Energy Component object that stores fuel. Contains values
    used to indicate its fuel type.
    """
    def __defaults__(self):
        self.tag                         = 'fuel_tank'
        self.fuel_selector_ratio         = 1.0
        self.mass_properties.empty_mass  = 0.0   
        self.fuel                        = None 