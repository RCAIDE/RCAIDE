## @ingroup Library-Attributes-Propellants
# RCAIDE/Library/Attributes/Propellants/Jet_A.py
# 
#
# Created:  Mar 2024, M. Clarke

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 

from .Propellant import Propellant
from RCAIDE.Framework.Core import Data

# ---------------------------------------------------------------------------------------------------------------------- 
#  Jet_A1 Propellant Class
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup  Library-Attributes-Propellants
class Jet_A(Propellant):
    """Jet A class propellant
    """

    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            Emission Indices from Lee, David S., et al. "The contribution of global aviation to anthropogenic climate forcing
            for 2000 to 2018." Atmospheric environment 244 (2021): 117834
            
            
            
            
        """    
        self.tag                          = 'Jet_A'
        self.reactant                     = 'O2'
        self.density                      = 820.0                          # kg/m^3 (15 C, 1 atm)
        self.specific_energy              = 43.02e6                        # J/kg
        self.energy_density               = 35276.4e6                      # J/m^3
        self.lower_heating_value          = 43.24e6                          # J/kg 
        self.max_mass_fraction            = Data({'Air' : 0.0633,'O2' : 0.3022})   # kg propellant / kg oxidizer
   
        # critical temperatures   
        self.temperatures.flash           = 311.15                 # K
        self.temperatures.autoignition    = 483.15                 # K
        self.temperatures.freeze          = 233.15                 # K
        self.temperatures.boiling         = 0.0                    # K 

        self.emission_indices.Production  = 0.4656   # kg/kg Greet 
        self.emission_indices.CO2         = 3.16    # kg/kg
        self.emission_indices.CO          = 0.00201 # kg/kg
        self.emission_indices.H2O         = 1.34    # kg/kg  
        self.emission_indices.SO2         = 0.0012  # kg/kg
        self.emission_indices.NOx         = 0.01514 # kg/kg
        self.emission_indices.Soot        = 0.0012  # kg/kg
        
        self.global_warming_potential_100.CO2       = 1     # CO2e/kg  
        self.global_warming_potential_100.H2O       = 0.06  # CO2e/kg  
        self.global_warming_potential_100.SO2       = -226  # CO2e/kg  
        self.global_warming_potential_100.NOx       = 52    # CO2e/kg  
        self.global_warming_potential_100.Soot      = 1166  # CO2e/kg    
        self.global_warming_potential_100.Contrails = 11 # kg/CO2e/km  