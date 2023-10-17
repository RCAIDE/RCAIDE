## @ingroup Attributes-Coolants
# Glycol_Water
#
# Created:  Dec. 2022,  C.R. Zhao

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
from .Coolant import Coolant

# ----------------------------------------------------------------------
#  Liquid H2 Cryogen Class
# ----------------------------------------------------------------------
## @ingroup Attributes-Coolants
class Glycol_Water(Coolant):
    """     """

    def __defaults__(self):
        """This sets the default values.

        Assumptions:
        We assume the mixture is 50%

        Source:

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """

        self.tag                       = 'Glycol_Water'
        self.percent_glycol            = 0.5 
        self.density                   = 1075                       # kg/m^3
        self.specific_heat_capacity    = 3300                       # J/kg.K
        self.thermal_conductivity      = 0.387                      # W/m.K
        self.dynamic_viscosity         = 0.0019                     # Pa.s
        self.Prandtl_number            = self.specific_heat_capacity * self.dynamic_viscosity / self.thermal_conductivity
        self.kinematic_viscosity       = self.dynamic_viscosity / self.density

    def compute_cp(self,T=300):
        # use engineering toolbox (https://www.engineeringtoolbox.com/ethylene-glycol-d_146.html) to create function 
        
        return self.specific_heat_capacity
    
    def compute_absolute_viscosity(self,T=300.,p=101325.):
        # use engineering toolbox (https://www.engineeringtoolbox.com/ethylene-glycol-d_146.html) to create function 
      
        return  self.dynamic_viscosity
    
    def compute_density(self,T=300.,p=101325.): 
        # use engineering toolbox (https://www.engineeringtoolbox.com/ethylene-glycol-d_146.html) to create function 
        
        return self.density  
    
    def compute_thermal_conductivity(self,T=300.,p=101325.): 
        # use engineering toolbox  http://www.mhtl.uwaterloo.ca/old/onlinetools/airprop/airprop.html
    
        return self.density  
    
    
    def compute_prandtl_number(self,T=300.): 
        Cp = self.compute_cp(T)
        mu = self.compute_absolute_viscosity(T)
        K  = self.compute_thermal_conductivity(T)
        return  mu*Cp/K      