## @ingroup Networks
# RCAIDE/Energy/Networks/Turbofan_Engine.py
# 
#
# Created:  Oct 2023, M. Clarke
# Modified: 

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------------------------------------------------------
# RCAIDE Imports  
import RCAIDE 
from RCAIDE.Core                                                             import Data 
from RCAIDE.Analyses.Mission.Common                                          import Residuals    
from RCAIDE.Methods.Propulsion.Performance.turbofan_propulsor                import turbofan_propulsor
from .Network                                                                import Network  
from .Network import Network

 # package imports 
import numpy as np  
from scipy.integrate import  cumtrapz 
 

# ----------------------------------------------------------------------------------------------------------------------
#  Turbofan
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks
class Turbofan_Engine(Network):
    """ This is a turbofan. 
    
        Assumptions:
        None
        
        Source:
        Most of the componentes come from this book:
        https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/
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

        self.tag                          = 'turbofan_engine'  
        self.system_voltage               = None   
        
    # linking the different network components
    def evaluate_thrust(self,state):
        """ Calculate thrust given the current state of the vehicle
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            state [state()]
    
            Outputs:
            results.thrust_force_vector [newtons]
            results.vehicle_mass_rate   [kg/s]
            conditions.noise.sources.turbofan:
                core:
                    exit_static_temperature      
                    exit_static_pressure       
                    exit_stagnation_temperature 
                    exit_stagnation_pressure
                    exit_velocity 
                fan:
                    exit_static_temperature      
                    exit_static_pressure       
                    exit_stagnation_temperature 
                    exit_stagnation_pressure
                    exit_velocity 
    
            Properties Used:
            Defaulted values
        """           

        #Unpack
        conditions  = state.conditions
        numerics    = state.numerics  
        fuel_lines  = self.fuel_lines 
         
        total_thrust  = 0. * state.ones_row(3) 
        total_power   = 0. * state.ones_row(1) 
        total_mdot    = 0. * state.ones_row(1) 
        
        for fuel_line in fuel_lines:
            fuel_tanks   = fuel_line.fuel_tanks    
            fuel_line_T , fuel_line_P, fuel_line_mdot  = turbofan_propulsor(fuel_line,state)    
        
            for fuel_tank in fuel_tanks: 
                fuel_line_results                                = conditions.energy[fuel_line.tag]  
                fuel_line_results[fuel_tank.tag].mass_flow_rate  = fuel_tank.fuel_selector_ratio*fuel_line_mdot 
                
            total_thrust += fuel_line_T   
            total_power  += fuel_line_P    
            total_mdot   += fuel_line_mdot    
    
        conditions.energy.thrust_force_vector  = total_thrust
        conditions.energy.power                = total_power 
        conditions.energy.vehicle_mass_rate    = total_mdot           
        
        # A PATCH TO BE DELETED IN RCAIDE
        results = Data()
        results.thrust_force_vector       = total_thrust
        results.power                     = total_power
        results.vehicle_mass_rate         = total_mdot     
        # -------------------------------------------------- 
        
        return results 
     
    
    def size(self,state):  
        """ Size the turbofan
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            State [state()]
    
            Outputs:
            None
    
            Properties Used:
            N/A
        """             
        
        #Unpack components
        conditions = state.conditions
        thrust     = self.thrust
        thrust.size(conditions) 
    
    def unpack_unknowns(self,segment):
        """Unpacks the unknowns set in the mission to be available for the mission.

        Assumptions:
        N/A
        
        Source:
        N/A
        
        Inputs:
        state.unknowns.rpm                   [rpm] 
        state.unknowns.throttle              [-] 
        
        Outputs:
        state.conditions.energy.rotor.rpm    [rpm] 
        state.conditions.energy.throttle     [-] 

        
        Properties Used:
        N/A
        """            
         
        if (type(segment) == RCAIDE.Analyses.Mission.Segments.Ground.Takeoff):
            pass
        elif (type(segment) == RCAIDE.Analyses.Mission.Segments.Ground.Landing):   
            pass
        elif (type(segment) == RCAIDE.Analyses.Mission.Segments.Cruise.Constant_Throttle_Constant_Altitude) or (type(segment) == RCAIDE.Analyses.Mission.Segments.Single_Point.Set_Speed_Set_Throttle):
            pass    
        else:
            fuel_lines   = segment.analyses.energy.networks.turbofan_engine.fuel_lines 
            for fuel_line_i, fuel_line in enumerate(fuel_lines):    
                fuel_line_results           = segment.state.conditions.energy[fuel_line.tag]  
                fuel_line_results.throttle  = segment.state.unknowns[fuel_line.tag + '_throttle']  
        
        return    
     
    def add_unknowns_and_residuals_to_segment(self,
                                              segment,
                                              estimated_throttles = [[1.0]]):
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
        fuel_lines  = segment.analyses.energy.networks.turbofan_engine.fuel_lines
        ones_row    = segment.state.ones_row 
        segment.state.residuals.network = Residuals() 
        
        if 'throttle' in segment.state.unknowns: 
            segment.state.unknowns.pop('throttle')
        if 'throttle' in segment.state.conditions.energy: 
            segment.state.conditions.energy.pop('throttle') 
         
        for fuel_line_i, fuel_line in enumerate(fuel_lines):    
            # ------------------------------------------------------------------------------------------------------            
            # Create fuel_line results data structure  
            # ------------------------------------------------------------------------------------------------------
            segment.state.conditions.energy[fuel_line.tag]       = RCAIDE.Analyses.Mission.Common.Conditions()       
            fuel_line_results                                    = segment.state.conditions.energy[fuel_line.tag]   
            fuel_line_results.throttle                           = 0. * ones_row(1) 
            segment.state.conditions.noise[fuel_line.tag]        = RCAIDE.Analyses.Mission.Common.Conditions()  
            noise_results                                        = segment.state.conditions.noise[fuel_line.tag]
            
            if (type(segment) == RCAIDE.Analyses.Mission.Segments.Ground.Takeoff):
                pass
            elif (type(segment) == RCAIDE.Analyses.Mission.Segments.Ground.Landing):   
                pass 
            elif (type(segment) == RCAIDE.Analyses.Mission.Segments.Cruise.Constant_Throttle_Constant_Altitude) or (type(segment) == RCAIDE.Analyses.Mission.Segments.Single_Point.Set_Speed_Set_Throttle):
                fuel_line_results.throttle = segment.throttle * ones_row(1)            
            else:       
                segment.state.unknowns[fuel_line.tag + '_throttle']  = estimated_throttles[fuel_line_i][0] * ones_row(1) 
     
            for fuel_tank in fuel_line.fuel_tanks:               
                fuel_line_results[fuel_tank.tag]                 = RCAIDE.Analyses.Mission.Common.Conditions()  
                fuel_line_results[fuel_tank.tag].mass_flow_rate  = ones_row(1)  
                fuel_line_results[fuel_tank.tag].mass            = ones_row(1)  
                
            # ------------------------------------------------------------------------------------------------------
            # Assign network-specific  residuals, unknowns and results data structures
            # ------------------------------------------------------------------------------------------------------
            for propulsor in fuel_line.propulsors:               
                fuel_line_results[propulsor.tag]                         = RCAIDE.Analyses.Mission.Common.Conditions()
                fuel_line_results[propulsor.tag].turbofan                = RCAIDE.Analyses.Mission.Common.Conditions()  
                fuel_line_results[propulsor.tag].y_axis_rotation         = 0. * ones_row(1)  
                fuel_line_results[propulsor.tag].turbofan.thrust         = 0. * ones_row(1) 
                fuel_line_results[propulsor.tag].turbofan.power          = 0. * ones_row(1) 
                noise_results[propulsor.tag]                             = RCAIDE.Analyses.Mission.Common.Conditions() 
                noise_results[propulsor.tag].turbofan                    = RCAIDE.Analyses.Mission.Common.Conditions() 
        
        segment.process.iterate.unknowns.network   = self.unpack_unknowns                   
        return segment    
        
    __call__ = evaluate_thrust
