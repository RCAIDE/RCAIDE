# RCAIDE/Framework/Networks/Turbofan_Engine_Network.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created:  Oct 2023, M. Clarke
# Modified: 

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE Imports  
import RCAIDE 
from RCAIDE.Library.Mission.Common.Unpack_Unknowns.energy import fuel_line_unknowns
from RCAIDE.Framework.Mission.Common                                                           import Residuals, Conditions
from RCAIDE.Library.Methods.Propulsors.Turbofan_Propulsor.compute_turbofan_performance  import compute_turbofan_performance
from .Network                                                                                  import Network  

# ----------------------------------------------------------------------------------------------------------------------
#  Turbofan
# ----------------------------------------------------------------------------------------------------------------------  
class Turbofan_Engine_Network(Network):
    """ This is a turbofan engine network
    """      
    
    def __defaults__(self):
        """ This sets the default values for the turbofan engine network.
    
            Assumptions:
            None
    
            Source:
            None 
        """            
        self.tag                          = 'turbofan_engine'  
        
    # linking the different network components
    def evaluate(self,state):
        """ Calculate thrust given the current state of the vehicle
    
            Assumptions:
                None
    
            Source:
                None
    
            Args:
                self  (dict): network           [-]  
                state (dict): flight conditions [-]  
    
            Returns:
                None 
        """           

        # Step 1: Unpack
        conditions  = state.conditions  
        fuel_lines  = self.fuel_lines 
         
        total_thrust  = 0. * state.ones_row(3) 
        total_power   = 0. * state.ones_row(1) 
        total_mdot    = 0. * state.ones_row(1)   
        
        # Step 2: loop through compoments of network and determine performance
        for fuel_line in fuel_lines:
            if fuel_line.active:   
                
                # Step 2.1: Compute and store perfomrance of all propulsors 
                fuel_line_T,fuel_line_P = compute_turbofan_performance(fuel_line,state)  
                total_thrust += fuel_line_T   
                total_power  += fuel_line_P  
                
                # Step 2.2: Link each turbofan the its respective fuel tank(s)
                for fuel_tank in fuel_line.fuel_tanks:
                    mdot = 0. * state.ones_row(1)   
                    for turbofan in fuel_line.propulsors:
                        for source in (turbofan.active_fuel_tanks):
                            if fuel_tank.tag == source: 
                                mdot += conditions.energy[fuel_line.tag][turbofan.tag].fuel_flow_rate 
                        
                    # Step 2.3 : Determine cumulative fuel flow from fuel tank 
                    fuel_tank_mdot = fuel_tank.fuel_selector_ratio*mdot + fuel_tank.secondary_fuel_flow 
                    
                    # Step 2.4: Store mass flow results 
                    conditions.energy[fuel_line.tag][fuel_tank.tag].mass_flow_rate  = fuel_tank_mdot  
                    total_mdot += fuel_tank_mdot                    
                            
        # Step 3: Pack results 
        conditions.energy.thrust_force_vector  = total_thrust
        conditions.energy.power                = total_power 
        conditions.energy.vehicle_mass_rate    = total_mdot 
            
        return 
     
    
    def size(self,state):  
        """ Size the turbofan
    
        Assumptions:
            None
    
        Source:
            None
    
        Args:
            self   : network           [-]
            state  : flight conditions [-]
     
        Returns:
            None 
        """             
        
        #Unpack components
        conditions = state.conditions
        thrust     = self.thrust
        thrust.size(conditions) 
    
    def unpack_unknowns(self,segment):
        """Unpacks the unknowns set in the mission to be available for the mission.

        Assumptions:
            None
        
        Source:
            None
        
        Args: 
            self    (dict): network                           [-]
            segment (dict): data structure of mission segment [-]
        
        Returns:
            None
        """            
         
        fuel_lines = segment.analyses.energy.networks.turbofan_engine.fuel_lines
        fuel_line_unknowns(segment,fuel_lines) 
            
        return    
     
    def add_unknowns_and_residuals_to_segment(self, segment):
        """ This function sets up the information that the mission needs to run a mission segment using this network 
         
        Assumptions:
            None
        
        Source:
            None
        
        Args: 
            self    (dict): network                           [-]
            segment (dict): data structure of mission segment [-]
        
        Returns:
            segment (dict): data structure of mission segment [-]
        """                  
        fuel_lines  = segment.analyses.energy.networks.turbofan_engine.fuel_lines
        ones_row    = segment.state.ones_row 
        segment.state.residuals.network = Residuals()  
        
        for fuel_line_i, fuel_line in enumerate(fuel_lines):    
            # ------------------------------------------------------------------------------------------------------            
            # Create fuel_line results data structure  
            # ------------------------------------------------------------------------------------------------------
            segment.state.conditions.energy[fuel_line.tag]       = Conditions()       
            fuel_line_results                                    = segment.state.conditions.energy[fuel_line.tag]    
            segment.state.conditions.noise[fuel_line.tag]        = Conditions()  
            noise_results                                        = segment.state.conditions.noise[fuel_line.tag]      
     
            for fuel_tank in fuel_line.fuel_tanks:               
                fuel_line_results[fuel_tank.tag]                 = Conditions()  
                fuel_line_results[fuel_tank.tag].mass_flow_rate  = ones_row(1)  
                fuel_line_results[fuel_tank.tag].mass            = ones_row(1)  
                
            # ------------------------------------------------------------------------------------------------------
            # Assign network-specific  residuals, unknowns and results data structures
            # ------------------------------------------------------------------------------------------------------
            for turbofan in fuel_line.propulsors:               
                fuel_line_results[turbofan.tag]                         = Conditions() 
                fuel_line_results[turbofan.tag].throttle                = 0. * ones_row(1)      
                fuel_line_results[turbofan.tag].y_axis_rotation         = 0. * ones_row(1)  
                fuel_line_results[turbofan.tag].thrust                  = 0. * ones_row(1) 
                fuel_line_results[turbofan.tag].power                   = 0. * ones_row(1) 
                noise_results[turbofan.tag]                             = Conditions() 
                noise_results[turbofan.tag].turbofan                    = Conditions() 
        
        segment.process.iterate.unknowns.network   = self.unpack_unknowns                   
        return segment    
        
    __call__ = evaluate
