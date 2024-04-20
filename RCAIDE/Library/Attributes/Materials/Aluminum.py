# @ingroup Library-Attributes-Solids 
# RCAIDE/Library/Attributes/Solids/Aluminum.py
# 
 

# Created: Mar 2024 M. Clarke

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from .Solid import Solid 

#-------------------------------------------------------------------------------
# Aluminum for WavyChannel for battery cooling
#-------------------------------------------------------------------------------

## @ingroup Attributes-Solid
class Aluminum(Solid): 
    """ Physical Constants Specific to 6061-T6 Aluminum
    """

    def __defaults__(self):
        """Sets material properties at instantiation. 

        Assumptions:
            None
    
        Source:
            Cao W, Zhao C, Wang Y, et al. Thermal modeling of full-size-scale cylindrical battery pack cooled
            by channeled liquid flow[J]. International journal of heat and mass transfer, 2019, 138: 1178-1187. 
        """

        self.density                    = 2719
        self.thermal_conductivity       = 202.4
        self.specific_heat_capacity     = 871
