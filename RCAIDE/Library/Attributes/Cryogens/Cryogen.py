## @ingroup Library-Attributes-Cryogens
# RCAIDE/Library/Attributes/Cryogens/Cryogens.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created:  Mar 2024, M. Clarke

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 

from RCAIDE.Frameworks.Core import Data

# ---------------------------------------------------------------------------------------------------------------------- 
# Cryogen
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Attributes-Cryogens
class Cryogen(Data):
    """Defauly cryogenic liquid class 
    
    Assumptions:
    None
    
    Source:
    None
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
        self.tag                       = 'Cryogen'
        self.density                   = 0.0                       # kg/m^3
        self.specific_energy           = 0.0                       # MJ/kg
        self.energy_density            = 0.0                       # MJ/m^3
        self.temperatures              = Data()
        self.temperatures.freeze       = 0.0                       # K
        self.temperatures.boiling      = 0.0                       # K