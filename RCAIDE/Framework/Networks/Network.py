# RCAIDE/Library/Compoments/Energy/Networks/Network.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created:  Jun 2024, M. Clarke
# Modified: Aug 2023, E. Botero


# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from RCAIDE.Framework.Core import Data
from RCAIDE.Library.Components import Component

# ----------------------------------------------------------------------------------------------------------------------
#  NETWORK
# ---------------------------------------------------------------------------------------------------------------------- 
class Network(Component):
    """ The top-level network class.
    """
    def __defaults__(self):
        """ This sets the default attributes for the network.
        
            Assumptions:
                None
            
            Source:
                None 
        """
        self.tag                                         = 'network'  
        self.busses                                      = Container()     
        self.fuel_lines                                  = Container()
        self.reverse_thrust                              = False
        self.wing_mounted                                = True

# ----------------------------------------------------------------------
#  Component Container
# ---------------------------------------------------------------------- 
class Container(Component.Container):
    """ The Network container class 
    """
    def evaluate(self,state):
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
        ones_row                          = state.ones_row
        results                           = Data()
        results.thrust_force_vector       = 0.*ones_row(3)
        results.vehicle_mass_rate         = 0.*ones_row(1)
        for net in self.values():
            if hasattr(net, 'has_additional_fuel_type'):
                if net.has_additional_fuel_type: 
                    results.vehicle_additional_fuel_rate  =  0.*ones_row(1)  
                    results.vehicle_fuel_rate             =  0.*ones_row(1)
            net.evaluate(state)
            results.thrust_force_vector  += state.conditions.energy.thrust_force_vector
            results.vehicle_mass_rate    += state.conditions.energy.vehicle_mass_rate    
        return results
    
# ----------------------------------------------------------------------
#  Handle Linking
# ----------------------------------------------------------------------
Network.Container = Container