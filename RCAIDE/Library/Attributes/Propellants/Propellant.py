## @ingroup Library-Attributes-Propellants 
# RCAIDE/Library/Attributes/Propellants.py
# 
# 
# Created:  Sep 2023, M. Clarke
# Modified: 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

from RCAIDE.Framework.Core import Data
from RCAIDE.Library.Components.Mass_Properties import Mass_Properties

# ----------------------------------------------------------------------------------------------------------------------
#  Propellant
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Attributes-Propellants  
class Propellant(Data):
    """Generic class for propellant
    """

    def __defaults__(self):
        """This sets the default values. 
    
        Assumptions:
            None
        
        Source:
            None
        """    
        self.tag                       = 'Propellant'
        self.reactant                  = 'O2'
        self.density                   = 0.0                       # kg/m^3
        self.specific_energy           = 0.0                       # MJ/kg
        self.energy_density            = 0.0                       # MJ/m^3
        self.mass_properties           = Mass_Properties()
        self.max_mass_fraction         = Data({'Air' : 0.0, 'O2' : 0.0}) # kg propellant / kg oxidizer
        self.temperatures              = Data()
        self.temperatures.flash        = 0.0                       # K
        self.temperatures.autoignition = 0.0                       # K
        self.temperatures.freeze       = 0.0                       # K
        self.temperatures.boiling      = 0.0                       # K