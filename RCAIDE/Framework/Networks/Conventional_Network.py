## @ingroup Networks
# RCAIDE/Energy/Networks/Conventional_Network.py
# 
#
# Created:  Jul 2024, S. Shekar


# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Library.Components              import Component
from RCAIDE.Library.Components.Component    import Container


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
        self.tag                    = 'conventional_network'
        self.distribution_lines     =  Container()
        self.wing_mounted           = True
        self.reverse_thrust         = False 
        
    def create_propulsion_network(self, Components,  fuel_line):
        """ Creates a Propulsion Network for each component pack in a given Propulsion Network
           
                   Assumptions:
                   N/A
           
                   Source:
                   N/A
           
                   Inputs:
                   Components that on that particular fuel line
                   Fuel line that components are connected to
                  
                   Outputs:
                   Creates a propulsion network
                   
                   Properties Used:
                   Defaulted values
               """        
        for Component in  Components:
            fuel_line[Component.type]                =  Container()
        for Component in  Components:     
            fuel_line[Component.type][Component.tag] =  Component
            
       