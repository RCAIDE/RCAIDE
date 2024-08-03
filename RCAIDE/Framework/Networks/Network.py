## @ingroup Networks
# RCAIDE/Energy/Networks/Network.py
# 
#
# Created:  Jul 2023, M. Clarke
# Modified: Aug 2023, E. Botero


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
class Network(Component):
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
        self.busses                 = Container()     
        self.fuel_lines             = Container()    
        self.wing_mounted           = True
        self.reverse_thrust         = False
        

# ----------------------------------------------------------------------
#  Component Container
# ---------------------------------------------------------------------- 
class Container(Component.Container):
    """ The Network container class 
    """
    def evaluate(self,state,center_of_gravity):
        """ This is used to evaluate the thrust produced by the network.
        
            Assumptions:  
                If multiple networks are attached their performances will be summed
            
            Source:
                None
            
            Args:
                State (dict): flight conditions 
            
            Returns:
                results (dict): Results of the evaluate method 
        """ 
        for net in self.values(): 
            net.evaluate(state,center_of_gravity)  
        return  
     
    
# ----------------------------------------------------------------------
#  Handle Linking
# ----------------------------------------------------------------------
Network.Container = Container