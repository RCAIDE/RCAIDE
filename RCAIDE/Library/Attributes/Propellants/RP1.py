## @ingroup Library-Attributes-Propellants 
# RCAIDE/Library/Attributes/RP1.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Sep 2023, M. Clarke
# Modified: 
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from .Propellant import Propellant
from RCAIDE.Framework.Core import Units

# ----------------------------------------------------------------------------------------------------------------------
#  RP1
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Attributes-Propellants
class RP1(Propellant):
    """RP1 Rocket Fuel Class
    
    Assumptions:
    Assumes an O/F ratio 2.27 
    
    Source:
    Sutton, Rocket Propulsion Elements
    """

    def __defaults__(self):
        """This sets the default values.

        Assumptions:
        None

        Source:
        Values commonly available

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """    
        self.tag                         = 'LOX_RP1'
        self.molecular_weight            = 22.193 # [kg/kmol]
        self.isentropic_expansion_factor = 1.1505
        self.combustion_temperature      = 3545.69*Units.kelvin             #[k]
        self.gas_specific_constant       = 8314.45986/self.molecular_weight*Units['J/(kg*K)']  # [J/(Kg-K)]