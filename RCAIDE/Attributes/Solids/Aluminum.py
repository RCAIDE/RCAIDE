# @ingroup Attributes-Solids

# Aluminum_Channel.py
#
# Created: Dec, 2022, C.R. Zhao

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from .Solid import Solid
from RCAIDE.Core import Units

#-------------------------------------------------------------------------------
# Aluminum for WavyChannel for battery cooling
#-------------------------------------------------------------------------------

## @ingroup Attributes-Solid
class Aluminum(Solid):

    """ Physical Constants Specific to 6061-T6 Aluminum

    Assumptions:
    None

    Source:
    Cao W, Zhao C, Wang Y, et al. Thermal modeling of full-size-scale cylindrical battery pack cooled
    by channeled liquid flow[J]. International journal of heat and mass transfer, 2019, 138: 1178-1187.

    Inputs:
    N/A

    Outputs:
    N/A

    Properties Used:
    None
    """

    def __defaults__(self):
        """Sets material properties at instantiation.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        N/A

        Outputs:
        N/A

        Properties Used:
        None
        """

        self.density                    = 2719
        self.thermal_conductivity       = 202.4
        self.specific_heat_capacity     = 871
