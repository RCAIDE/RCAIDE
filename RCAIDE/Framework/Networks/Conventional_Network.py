## @ingroup Networks
# RCAIDE/Energy/Networks/Conventional_Network.py
# 
#
# Created:  Jul 2024, S. Shekar


# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from RCAIDE.Library.Components import Component  
from RCAIDE.Framework.Core import Data
from RCAIDE.Library.Components import Component

# ----------------------------------------------------------------------------------------------------------------------
#  NETWORK
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Energy-Networks
class Conventional_Network(Component):
    """ RCAIDE.Energy.Networks.Network()
        The Top Level Network Class
            Assumptions:
            None
            Source:
            N/As
    """
    def __defaults__(self):
        """ This sets the default attributes for the network.
                Assumptions:
                None
                Source:
                N/A
                Inputs:
                None
                Outputs:
                None
                Properties Used:
                N/A
        """
        self.tag                    = 'network'  
        self.fuel_lines             = Container()    
        self.wing_mounted           = True
        self.reverse_thrust         = False 
