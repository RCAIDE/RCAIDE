## @ingroup Networks
# RCAIDE/Energy/Networks/Turbojet_Engine.py
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
from RCAIDE.Methods.Propulsion.turbojet_propulsor                            import compute_propulsor_performance , compute_unique_propulsor_groups 
from .Network                                                                import Network  
from .Network import Network

 # package imports 
import numpy as np  
from scipy.integrate import  cumtrapz 
 

# ----------------------------------------------------------------------------------------------------------------------
#  Turbojet 
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Energy-Networks
class Turbojet_Engine(Network):
    """ This is a turbojet. 
    
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

        self.tag                          = 'turbojet_engine'  
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
            conditions.noise.sources.turbojet:
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
        total_power   = 0.
        total_mdot    = 0.
        
        for fuel_line in fuel_lines:
            fuel_tanks = fuel_line.fuel_tanks
            turbojets  = fuel_line.turbojets  
            fuel_line_mdot  = 0   
            fuel_line_T     = 0   
            fuel_line_P     = 0               
            for i in range(conditions.energy[fuel_line.tag].number_of_propulsor_groups):
                if fuel_line.active_propulsor_groups[i]:           
                    pg_tag      = conditions.energy[fuel_line.tag].active_propulsor_groups[i]
                    N_turbojets = conditions.energy[fuel_line.tag].N_turbojets
                    T , P, mdot = compute_propulsor_performance(i,fuel_line,pg_tag,turbojets,N_turbojets,conditions)     
                    fuel_line_T            += T       
                    fuel_line_P            += P  
                    fuel_line_mdot         += mdot 
        
                    conditions.energy[fuel_line.tag][pg_tag].turbojet.thrust = fuel_line_T   
                    conditions.energy[fuel_line.tag][pg_tag].turbojet.power  = fuel_line_P                     
        
            for fuel_tank in fuel_tanks: 
                fuel_line_results                                = conditions.energy[fuel_line.tag]                
                fuel_line_results[fuel_tank.tag].mass_flow_rate  = fuel_tank.fuel_selector_ratio*fuel_line_mdot
                fuel_line_results[fuel_tank.tag].mass            = np.atleast_2d((fuel_line_results[fuel_tank.tag].mass[0,0] - cumtrapz(fuel_line_results[fuel_tank.tag].mass_flow_rate[:,0], x   = numerics.time.control_points[:,0]))).T
                
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
        """ Size the turbojet
    
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
 
        fuel_lines   = segment.analyses.energy.networks.turbojet_engine.fuel_lines 
        for fuel_line in fuel_lines: 
            fuel_line_results       = segment.state.conditions.energy[fuel_line.tag] 
            active_propulsor_groups = fuel_line_results.active_propulsor_groups
            for i in range(len(active_propulsor_groups)): 
                pg_tag = active_propulsor_groups[i]            
                fuel_line_results[pg_tag].turbojet.throttle  = segment.state.unknowns[fuel_line.tag + '_' + pg_tag + '_throttle']  
        
        return    
     
    def add_unknowns_and_residuals_to_segment(self,
                                              segment,
                                              estimated_propulsor_group_throttles = [[0.5]]):
        """ This function sets up the information that the mission needs to run a mission segment using this network 
         
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            segment
            eestimated_propulsor_group_throttles           [-]
            estimated_propulsor_group_rpms                 [-]  
            
            Outputs:
            segment
    
            Properties Used:
            N/A
        """                  
        fuel_lines   = segment.analyses.energy.networks.turbojet_engine.fuel_lines
        ones_row    = segment.state.ones_row 
        segment.state.residuals.network = Residuals() 
        
        if 'throttle' in segment.state.unknowns: 
            segment.state.unknowns.pop('throttle')
        if 'throttle' in segment.state.conditions.energy: 
            segment.state.conditions.energy.pop('throttle')
         
        for fuel_line_i, fuel_line in enumerate(fuel_lines):  
            active_propulsor_groups   = fuel_line.active_propulsor_groups 
            N_active_propulsor_groups = len(active_propulsor_groups)
            fuel_tanks                = fuel_line.fuel_tanks

            # ------------------------------------------------------------------------------------------------------            
            # Create fuel_line results data structure  
            # ------------------------------------------------------------------------------------------------------
            segment.state.conditions.energy[fuel_line.tag] = RCAIDE.Analyses.Mission.Common.Conditions()            

            # ------------------------------------------------------------------------------------------------------            
            # Determine number of propulsor groups in fuel_line
            # ------------------------------------------------------------------------------------------------------
            sorted_propulsors                             = compute_unique_propulsor_groups(fuel_line)
            fuel_line_results                             = segment.state.conditions.energy[fuel_line.tag]
            fuel_line_results.number_of_propulsor_groups  = N_active_propulsor_groups
            fuel_line_results.active_propulsor_groups     = active_propulsor_groups
            fuel_line_results.N_turbojets                 = sorted_propulsors.N_turbojets
     
            for fuel_tank in fuel_tanks:               
                fuel_line_results[fuel_tank.tag]                 = RCAIDE.Analyses.Mission.Common.Conditions()  
                fuel_line_results[fuel_tank.tag].mass_flow_rate  = ones_row(1)  
                fuel_line_results[fuel_tank.tag].mass            = ones_row(1)  
                
            # ------------------------------------------------------------------------------------------------------
            # Assign network-specific  residuals, unknowns and results data structures1
            # ------------------------------------------------------------------------------------------------------
            for i in range(len(sorted_propulsors.unique_turbojet_tags)):         
                segment.state.unknowns[fuel_line.tag + '_' + active_propulsor_groups[i] + '_throttle']    = estimated_propulsor_group_throttles[fuel_line_i][i] * ones_row(1)     
                                 
                # Results data structure for each propulsor group    
                pg_tag                                            = active_propulsor_groups[i] 
                fuel_line_results[pg_tag]                         = RCAIDE.Analyses.Mission.Common.Conditions()
                fuel_line_results[pg_tag].turbojet                = RCAIDE.Analyses.Mission.Common.Conditions() 
                fuel_line_results[pg_tag].unique_turbojet_tags    = sorted_propulsors.unique_turbojet_tags
                fuel_line_results[pg_tag].y_axis_rotation         = 0. * ones_row(1) 
                fuel_line_results[pg_tag].turbojet.thrust         = 0. * ones_row(1) 
                fuel_line_results[pg_tag].turbojet.power          = 0. * ones_row(1) 
                fuel_line_results[pg_tag].turbojet.thottle        = 0. * ones_row(1) 
        
        segment.process.iterate.unknowns.network                  = self.unpack_unknowns                   
        return segment    
        
    __call__ = evaluate_thrust 
 