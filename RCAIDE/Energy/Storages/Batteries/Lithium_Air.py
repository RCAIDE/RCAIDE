# RCAIDE/Energy/Storages/Batteries/Lithium_Air.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Core import Units
from RCAIDE.Energy.Storages.Batteries  import Battery

# ----------------------------------------------------------------------------------------------------------------------
#  BATTERY
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Energy-Storages-Batteries 
class Lithium_Air(Battery):
    """
    Specifies specific energy characteristics specific to
    lithium-air batteries. Also includes parameters related to 
    consumption of oxygen
    """
    
    
    def __defaults__(self):
        self.specific_energy  = 2000.     *Units.Wh/Units.kg    # convert to Joules/kg
        self.specific_power   = 0.66      *Units.kW/Units.kg    # convert to W/kg
        self.mass_gain_factor = (1.92E-4) /Units.Wh
       
            
  