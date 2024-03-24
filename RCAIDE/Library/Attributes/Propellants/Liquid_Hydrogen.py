## @ingroup Library-Attributes-Propellants 
# RCAIDE/Library/Attributes/Liquid_Hydrogen.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Sep 2023, M. Clarke
# Modified: 
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from .Propellant import Propellant 

# ----------------------------------------------------------------------------------------------------------------------
#  Liquid Hydrogen
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Attributes-Propellants
class Liquid_Hydrogen(Propellant):
    """Liquid hydrogen fuel
    
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
        http://arc.uta.edu/publications/td_files/Kristen%20Roberts%20MS.pdf

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """ 
        
        self.tag                        = 'Liquid_H2' 
        self.reactant                   = 'O2' 
        self.density                    = 59.9                             # [kg/m^3] 
        self.specific_energy            = 141.86e6                         # [J/kg] 
        self.energy_density             = 8491.0e6                         # [J/m^3] 
        self.stoichiometric_fuel_to_air = 0.0291 
        self.temperatures.autoignition  = 845.15                           # [K]         