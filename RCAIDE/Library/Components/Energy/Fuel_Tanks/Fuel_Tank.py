## @ingroup Library-Compoments-Energy-Fuel_Tanks Fuel_Tanks
# RCAIDE/Library/Compoments/Energy/Fuel_Tanks/Fuel_Tank.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Library.Components    import Component   

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Tank
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Library-Compoments-Energy-Fuel_Tanks 
class Fuel_Tank(Component):
    """Fuel tank compoment.
    """
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """          
        self.tag                         = 'fuel_tank'
        self.type                        = 'fuel_tanks'
        self.fuel_selector_ratio         = 1.0 
        self.mass_properties.empty_mass  = 0.0   
        self.secondary_fuel_flow         = 0.0
        self.fuel                        = None 