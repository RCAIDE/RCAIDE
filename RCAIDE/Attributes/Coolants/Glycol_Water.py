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
    """Holds values for this liquid coolant

    Assumptions:
    None

    Source:
    Cao W, Zhao C, Wang Y, et al. Thermal modeling of full-size-scale cylindrical battery pack cooled by channeled
    liquid flow[J]. International journal of heat and mass transfer, 2019, 138: 1178-1187.
    """

    def __defaults__(self):
        """This sets the default values.

        Assumptions:
        Ambient Pressure

        Source:

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """

        self.tag                        = 'Glycol_Water'
        self.density                   = 1075                       # kg/m^3
        self.specific_heat_capacity    = 3300                       # J/kg.K
        self.thermal_conductivity      = 0.387                      # W/m.K
        self.dynamic_viscosity         = 0.0019                     # Pa.s
        self.Prandtl_number            = self.specific_heat_capacity * self.dynamic_viscosity / self.thermal_conductivity
        self.kinematic_viscosity       = self.dynamic_viscosity / self.density
