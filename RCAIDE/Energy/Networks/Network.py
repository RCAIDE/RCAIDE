## @ingroup Networks
# RCAIDE/Energy/Networks/Network.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created:  Jul 2023, M. Clarke
# Modified: Aug 2023, E. Botero


# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from RCAIDE.Energy import Energy_Component
from RCAIDE.Core import Data
from RCAIDE.Components import Component

# ----------------------------------------------------------------------------------------------------------------------
#  NETWORK
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Energy-Networks
class Network(Energy_Component):
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

# ----------------------------------------------------------------------
#  Component Container
# ----------------------------------------------------------------------
## @ingroup Energy-Network
class Container(Component.Container):
    """ RCAIDE.Components.Energy.Networks.Network.Container()
        The Network Container Class
            Assumptions:
            None
            Source:
            N/A
    """
    def evaluate_thrust(self,state):
        """ This is used to evaluate the thrust produced by the network.
                Assumptions:
                Network has "evaluate_thrust" method
                If multiple networks are attached their masses will be summed
                Source:
                N/A
                Inputs:
                State variables
                Outputs:
                Results of the "evaluate_thrust" method
                Properties Used:
                N/A
        """
        ones_row = state.ones_row
        results = Data()
        results.thrust_force_vector       = 0.*ones_row(3)
        results.vehicle_mass_rate         = 0.*ones_row(1)
        for net in self.values():
            if hasattr(net, 'has_additional_fuel_type'):
                if net.has_additional_fuel_type: #Check if Network has additional fuel
                    results.vehicle_additional_fuel_rate  =  0.*ones_row(1) #fuel rate for additional fuel types, eg cryogenic fuel
                    results.vehicle_fuel_rate             =  0.*ones_row(1)
            results_p = net.evaluate_thrust(state)
            for key in results.keys():
                results[key] += results_p[key]
        return results
    
# ----------------------------------------------------------------------
#  Handle Linking
# ----------------------------------------------------------------------
Network.Container = Container