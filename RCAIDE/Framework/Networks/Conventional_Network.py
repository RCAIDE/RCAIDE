## @ingroup Networks
# RCAIDE/Energy/Networks/Conventional_Network.py
# 
#
# Created:  Jul 2024, S. Shekar


# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE
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
            
    def unpack_unknowns(self,segment):
        """Unpacks the unknowns set in the mission to be available for the mission.

        Assumptions:
        N/A
        
        Source:
        N/A
        
        Inputs: 
            segment   - data structure of mission segment [-]
        
        Outputs: 
        
        Properties Used:
        N/A
        """            
         
        fuel_lines = segment.analyses.energy.networks.turbofan_engine.fuel_lines
        RCAIDE.Library.Mission.Common.Unpack_Unknowns.energy.fuel_line_unknowns(segment,fuel_lines) 
            
        return
  
    def add_unknowns_and_residuals_to_segment(self, segment):
        """ This function sets up the information that the mission needs to run a mission segment using this network 
         
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            segment
            eestimated_throttles           [-]
            estimated_propulsor_group_rpms [-]  
            
            Outputs:
            segment
    
            Properties Used:
            N/A
        """                  
        
        segment.process.iterate.unknowns.network   = self.unpack_unknowns                   
        return segment        
            
       