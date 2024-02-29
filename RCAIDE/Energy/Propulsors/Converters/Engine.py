## @ingroup Energy-Propulsors-Converters
# RCAIDE/Energy/Propulsors/Converters/Engine.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports  
from RCAIDE.Energy.Energy_Component                      import Energy_Component   

# ---------------------------------------------------------------------------------------------------------------------- 
#  Engine Class
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Energy-Propulsors-Converters
class Engine(Energy_Component):
    """This is an internal combustion engine component.
    
    Assumptions:
    None

    Source:
    None
    """           
    def __defaults__(self):
        self.tag                             = 'internal_combustion_engine' 
        self.sea_level_power                 = 0.0
        self.flat_rate_altitude              = 0.0
        self.rated_speed                     = 0.0 
        self.inputs.speed                    = 0.0
        self.power_split_ratio               = 0.0
        self.power_specific_fuel_consumption = 0.36

