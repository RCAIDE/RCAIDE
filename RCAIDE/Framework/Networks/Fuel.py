## @ingroup Networks
# RCAIDE/Energy/Networks/Fuel.py
# 
# Created:  Oct 2023, M. Clarke
# Modified: 

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------------------------------------------------------
# RCAIDE Imports
import  RCAIDE 
from RCAIDE.Framework.Mission.Common                      import Residuals , Conditions 
from RCAIDE.Library.Mission.Common.Unpack_Unknowns.energy import fuel_line_unknowns
from .Network                                             import Network  
#from RCAIDE.Library.Components                            import Component
#from RCAIDE.Library.Components.Component                  import Container


# ----------------------------------------------------------------------------------------------------------------------
# Fuel
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks
class Fuel(Network):
    """ This is a  fuel-based network. 
    
        Assumptions:
        None
        
        Source: 
    """      
    
    def __defaults__(self):
        """ This sets the default values for the network to function.
    
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

        self.tag    = 'fuel'  
        
    # linking the different network components
    def evaluate_thrust(self,state,center_of_gravity):
        """ Calculate thrust given the current state of the vehicle
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs: 
    
            Outputs:  
        """           

        # Step 1: Unpack
        conditions     = state.conditions  
        fuel_lines     = self.fuel_lines 
        reverse_thrust = self.reverse_thrust
        total_thrust   = 0. * state.ones_row(3) 
        total_moment   = 0. * state.ones_row(3) 
        total_power    = 0. * state.ones_row(1) 
        total_mdot     = 0. * state.ones_row(1)   
        
        # Step 2: loop through compoments of network and determine performance
        for fuel_line in fuel_lines:
            if fuel_line.active:     
                stored_results_flag  = False
                stored_propulsor_tag = None 
                for propulsor in fuel_line.propulsors:  
                    if propulsor.active == True:  
                        if fuel_line.identical_propulsors == False:
                            # run analysis  
                            T,M,P,stored_results_flag,stored_propulsor_tag = propulsor.compute_performance(state,fuel_line,center_of_gravity)
                        else:             
                            if stored_results_flag == False: 
                                # run propulsor analysis 
                                T,M,P,stored_results_flag,stored_propulsor_tag = propulsor.compute_performance(state,fuel_line,center_of_gravity)
                            else:
                                # use previous propulsor results 
                                T,M,P = propulsor.reuse_stored_data(state,fuel_line,stored_propulsor_tag,center_of_gravity)
                          
                        total_thrust += T   
                        total_moment += M   
                        total_power  += P  
                
                # Step 2.2: Link each propulsor the its respective fuel tank(s)
                for fuel_tank in fuel_line.fuel_tanks:
                    mdot = 0. * state.ones_row(1)   
                    for propulsor in fuel_line.propulsors:
                        for source in (propulsor.active_fuel_tanks):
                            if fuel_tank.tag == source: 
                                mdot += conditions.energy[fuel_line.tag][propulsor.tag].fuel_flow_rate 
                        
                    # Step 2.3 : Determine cumulative fuel flow from fuel tank 
                    fuel_tank_mdot = fuel_tank.fuel_selector_ratio*mdot + fuel_tank.secondary_fuel_flow 
                    
                    # Step 2.4: Store mass flow results 
                    conditions.energy[fuel_line.tag][fuel_tank.tag].mass_flow_rate  = fuel_tank_mdot  
                    total_mdot += fuel_tank_mdot                    
                            
        # Step 3: Pack results
        if reverse_thrust ==  True:
            total_thrust =  total_thrust* -1
            total_moment =  total_moment* -1
            
        conditions.energy.thrust_force_vector  = total_thrust
        conditions.energy.thrust_moment_vector = total_moment
        conditions.energy.power                = total_power 
        conditions.energy.vehicle_mass_rate    = total_mdot    
        
        return
    
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
         
        fuel_lines = segment.analyses.energy.vehicle.networks.fuel.fuel_lines
        fuel_line_unknowns(segment,fuel_lines) 
            
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
        fuel_lines  = segment.analyses.energy.vehicle.networks.fuel.fuel_lines
        ones_row    = segment.state.ones_row 
        segment.state.residuals.network = Residuals()  

        # ------------------------------------------------------------------------------------------------------            
        # Create fuel_line results data structure  
        # ------------------------------------------------------------------------------------------------------        
        for fuel_line_i, fuel_line in enumerate(fuel_lines):    
            # ------------------------------------------------------------------------------------------------------            
            # Create fuel_line results data structure  
            # ------------------------------------------------------------------------------------------------------
            segment.state.conditions.energy[fuel_line.tag] = Conditions()        
            segment.state.conditions.noise[fuel_line.tag]  = Conditions()     
     
            for fuel_tank in fuel_line.fuel_tanks:               
                segment.state.conditions.energy[fuel_line.tag][fuel_tank.tag]                 = Conditions()  
                segment.state.conditions.energy[fuel_line.tag][fuel_tank.tag].mass_flow_rate  = ones_row(1)  
                segment.state.conditions.energy[fuel_line.tag][fuel_tank.tag].mass            = ones_row(1)  
                
            # ------------------------------------------------------------------------------------------------------
            # Assign network-specific  residuals, unknowns and results data structures
            # ------------------------------------------------------------------------------------------------------
            for propulsor in fuel_line.propulsors:
                propulsor.append_operating_conditions(segment,fuel_line) 
                for tag, item in  propulsor.items(): 
                    if issubclass(type(item), RCAIDE.Library.Components.Component):
                        item.append_operating_conditions(segment,fuel_line,propulsor)  
        segment.process.iterate.unknowns.network   = self.unpack_unknowns                   
        return segment    
        
    __call__ = evaluate_thrust 

  
## ----------------------------------------------------------------------------------------------------------------------
##  NETWORK
## ----------------------------------------------------------------------------------------------------------------------
### @ingroup Energy-Networks
#class Conventional_Network(Component):
    #""" RCAIDE.Energy.Networks.Network()
        #The Top Level Network Class
            #Assumptions:
            #None
            #Source:
            #N/As
    #"""
    #def __defaults__(self):
        #""" This sets the default attributes for the network.
                #Assumptions:
                #None
                #Source:
                #N/A
                #Inputs:
                #None
                #Outputs:
                #None
                #Properties Used:
                #N/A
        #"""
        #self.tag                    = 'conventional_network'
        #self.distribution_lines     =  Container()
        #self.wing_mounted           = True
        
        
     
    #def create_propulsion_network(self, Components,  fuel_line):
        #""" Creates a Propulsion Network for each component pack in a given Propulsion Network
           
                   #Assumptions:
                   #N/A
           
                   #Source:
                   #N/A
           
                   #Inputs:
                   #Components that on that particular fuel line
                   #Fuel line that components are connected to
                  
                   #Outputs:
                   #Creates a propulsion network
                   
                   #Properties Used:
                   #Defaulted values
               #"""        
        #for Component in  Components:
            #fuel_line[Component.type]                =  Container()
        #for Component in  Components:     
            #fuel_line[Component.type][Component.tag] =  Component
            
    #def unpack_unknowns(self,segment):
        #"""Unpacks the unknowns set in the mission to be available for the mission.

        #Assumptions:
        #N/A
        
        #Source:
        #N/A
        
        #Inputs: 
            #segment   - data structure of mission segment [-]
        
        #Outputs: 
        
        #Properties Used:
        #N/A
        #"""            
         
        #fuel_lines = segment.analyses.energy.networks.turbofan_engine.fuel_lines
        #RCAIDE.Library.Mission.Common.Unpack_Unknowns.energy.fuel_line_unknowns(segment,fuel_lines) 
            
        #return
  
    #def add_unknowns_and_residuals_to_segment(self, segment):
        #""" This function sets up the information that the mission needs to run a mission segment using this network 
         
            #Assumptions:
            #None
    
            #Source:
            #N/A
    
            #Inputs:
            #segment
            #eestimated_throttles           [-]
            #estimated_propulsor_group_rpms [-]  
            
            #Outputs:
            #segment
    
            #Properties Used:
            #N/A
        #"""                  
        
        #segment.process.iterate.unknowns.network   = self.unpack_unknowns                   
        #return segment        
            
       