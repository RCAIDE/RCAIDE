# RCAIDE/Library/Attributes/Propellants/Liquid_Natural_Gas.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created: Mar 2024, RCAIDE Team

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 

from .Propellant import Propellant   

# ---------------------------------------------------------------------------------------------------------------------- 
#  Gaseous_Hydrogen Class
# ----------------------------------------------------------------------------------------------------------------------   
class Liquid_Natural_Gas(Propellant):
    """Liquid natural gas fuel class,
    """

    def __defaults__(self):
        """This sets the default values. 
    
    Assumptions:
        None
    
    Source:
        None
        """    
        self.tag             = 'Liquid_Natural_Gas'
        self.reactant        = 'O2'
        self.density         = 414.2                            # kg/m^3 
        self.specific_energy = 53.6e6                           # J/kg
        self.energy_density  = 22200.0e6                        # J/m^3