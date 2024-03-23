## @ingroup Library-Attributes-Propellants
# RCAIDE/Library/Attributes/Propellants/Jet_A.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created:  Mar 2024, M. Clarke

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 

from .Propellant import Propellant
from RCAIDE.Frameworks.Core import Data

# ---------------------------------------------------------------------------------------------------------------------- 
#  Jet_A1 Propellant Class
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup  Library-Attributes-Propellants
class Jet_A(Propellant):
    """Jet A class propellant 
    
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
        self.tag                       = 'Jet_A'
        self.reactant                  = 'O2'
        self.density                   = 820.0                          # kg/m^3 (15 C, 1 atm)
        self.specific_energy           = 43.02e6                        # J/kg
        self.energy_density            = 35276.4e6                      # J/m^3
        self.max_mass_fraction         = Data({'Air' : 0.0633,'O2' : 0.3022})   # kg propellant / kg oxidizer

        # critical temperatures
        self.temperatures.flash        = 311.15                 # K
        self.temperatures.autoignition = 483.15                 # K
        self.temperatures.freeze       = 233.15                 # K
        self.temperatures.boiling      = 0.0                    # K