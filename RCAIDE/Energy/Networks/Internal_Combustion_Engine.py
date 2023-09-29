## @ingroup Energy-Networks
# RCAIDE/Energy/Networks/Internal_Combustion_Engine.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports 
import RCAIDE 
from RCAIDE.Core                                                    import Data 
from RCAIDE.Analyses.Mission.Common                                 import Residuals 
from RCAIDE.Components.Component                                    import Container    
from RCAIDE.Methods.Propulsion.internal_combustion_engine_propulsor import compute_propulsor_performance ,compute_unique_propulsor_groups 
from .Network                                                       import Network  

# python imports 
import numpy as np 
from scipy.integrate import  cumtrapz

# ----------------------------------------------------------------------------------------------------------------------
#  ICE_Propelle
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks
class Internal_Combustion_Engine(Network):
    """ A network comprising fuel tank(s) to power propeller driven engines via a fuel line.
        Avionics, paylaods are also modelled. Rotors and engines are arranged into groups,
        called propulsor groups, to siginify how they are connected in the network.  
        This network adds additional unknowns and residuals to the mission to determinge 
        the torque matching between engine and rotors in each propulsor group.  
    
        Assumptions:
        None
        
        Source:
        None
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
        self.tag                          = 'internal_combustion_engine'  
        self.avionics                     = None
        self.payload                      = None 
    
    # manage process with a driver function
    def evaluate_thrust(self,state):
        """ Calculate thrust given the current state of the vehicle
    
            Assumptions:
    
            Source:
            N/A
    
            Inputs:
            state [state()]
    
            Outputs:
            results.thrust_force_vector         [newtons]
            results.vehicle_mass_rate           [kg/s]
            conditions.energy                   [-]    
    
            Properties Used:
            Defaulted values
        """           
        # unpack
        conditions   = state.conditions 
        numerics     = state.numerics
        fuel_lines   = self.fuel_lines 

        total_thrust = 0. * state.ones_row(3)
        total_power  = 0. 
        total_mdot   = 0.
        
        for fuel_line in fuel_lines:     
            engines    = fuel_line.engines
            rotors     = fuel_line.rotors 
            fuel_tanks = fuel_line.fuel_tanks

            fuel_line_mdot  = 0   
            fuel_line_T     = 0   
            fuel_line_P     = 0   
            for i in range(conditions.energy[fuel_line.tag].number_of_propulsor_groups):
                if fuel_line.active_propulsor_groups[i]:           
                    pg_tag                 = conditions.energy[fuel_line.tag].active_propulsor_groups[i]
                    N_rotors               = conditions.energy[fuel_line.tag].N_rotors
                    outputs , T , P, mdot  = compute_propulsor_performance(i,fuel_line.tag,pg_tag,engines,rotors,N_rotors,conditions)   
                    fuel_line_T            += T       
                    fuel_line_P            += P  
                    fuel_line_mdot         += mdot
        
                    conditions.energy[fuel_line.tag][pg_tag].engine.thrust = fuel_line_T   
                    conditions.energy[fuel_line.tag][pg_tag].engine.power  = fuel_line_P 
                    
            for fuel_tank in fuel_tanks: 
                fuel_line_results        = conditions.energy[fuel_line.tag]                
                fuel_line_results[fuel_tank.tag].mass_flow_rate  = fuel_tank.fuel_selector_ratio*fuel_line_mdot
                fuel_line_results[fuel_tank.tag].mass            = np.atleast_2d((fuel_line_results[fuel_tank.tag].mass[0,0] - cumtrapz(fuel_line_results[fuel_tank.tag].mass_flow_rate[:,0], x   = numerics.time.control_points[:,0]))).T
              
            total_thrust += fuel_line_T   
            total_power  += fuel_line_P   
            total_mdot   += fuel_line_mdot
    
        conditions.energy.thrust_force_vector  = total_thrust
        conditions.energy.power                = total_power 
        conditions.energy.vehicle_mass_rate    = total_mdot  
        
        # --------------------------------------------------
        # A PATCH TO BE DELETED IN RCAIDE
        results = Data()
        results.thrust_force_vector       = total_thrust
        results.power                     = total_power
        results.vehicle_mass_rate         = total_mdot   
        # --------------------------------------------------
        
        return results 
    
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
 
        fuel_lines   = segment.analyses.energy.networks.internal_combustion_engine.fuel_lines 
        for fuel_line in fuel_lines: 
            fuel_line_results       = segment.state.conditions.energy[fuel_line.tag] 
            active_propulsor_groups = fuel_line_results.active_propulsor_groups
            for i in range(len(active_propulsor_groups)): 
                pg_tag = active_propulsor_groups[i]           
                fuel_line_results[pg_tag].rotor.rpm        = segment.state.unknowns[fuel_line.tag + '_' + pg_tag + '_rpm']  
                fuel_line_results[pg_tag].engine.throttle  = segment.state.unknowns[fuel_line.tag + '_' + pg_tag + '_throttle']  
        
        return
    
    def residuals(self,segment):
        """ Calculates a residual based on torques 
        
        Assumptions:
        
        Inputs:
            segment.state.conditions.energy.
                engine.torque                       [newtom-meters]                 
                rotor.torque                        [newtom-meters] 
        
        Outputs:
            segment.state: 
                residuals.network                   [newtom-meters] 
                
        Properties Used:
            N/A
                                
        """     
        
        fuel_lines   = segment.analyses.energy.networks.internal_combustion_engine.fuel_lines 
        for fuel_line in fuel_lines:  
            fuel_line_results       = segment.state.conditions.energy[fuel_line.tag] 
            active_propulsor_groups = fuel_line_results.active_propulsor_groups
            for i in range(len(active_propulsor_groups)):  
                q_engine   = fuel_line_results[active_propulsor_groups[i]].engine.torque
                q_prop    = fuel_line_results[active_propulsor_groups[i]].rotor.torque 
                segment.state.residuals.network[fuel_line.tag + '_' + active_propulsor_groups[i] + '_rotor_engine_torque'] = q_engine - q_prop 
        
        return
    
    def add_unknowns_and_residuals_to_segment(self,
                                              segment,
                                              estimated_propulsor_group_throttles = [[0.5]], 
                                              estimated_propulsor_group_rpms      = [[2500]]):
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
        fuel_lines   = segment.analyses.energy.networks.internal_combustion_engine.fuel_lines
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
            fuel_line_results.N_rotors                    = sorted_propulsors.N_rotors
     
            for fuel_tank in fuel_tanks:               
                fuel_line_results[fuel_tank.tag]                 = RCAIDE.Analyses.Mission.Common.Conditions()  
                fuel_line_results[fuel_tank.tag].mass_flow_rate  = ones_row(1)  
                fuel_line_results[fuel_tank.tag].mass            = ones_row(1)  
                
            # ------------------------------------------------------------------------------------------------------
            # Assign network-specific  residuals, unknowns and results data structures
            # ------------------------------------------------------------------------------------------------------
            for i in range(len(sorted_propulsors.unique_rotor_tags)):        
                segment.state.unknowns[fuel_line.tag + '_' + active_propulsor_groups[i] + '_rpm']                           = estimated_propulsor_group_rpms[fuel_line_i][i] * ones_row(1)  
                segment.state.residuals.network[ fuel_line.tag + '_' + active_propulsor_groups[i] + '_rotor_engine_torque'] = 0. * ones_row(1)      
                segment.state.unknowns[fuel_line.tag + '_' + active_propulsor_groups[i] + '_throttle']                      = estimated_propulsor_group_throttles[fuel_line_i][i] * ones_row(1)     
                                 
                # Results data structure for each propulsor group    
                pg_tag                                            = active_propulsor_groups[i] 
                fuel_line_results[pg_tag]                         = RCAIDE.Analyses.Mission.Common.Conditions()
                fuel_line_results[pg_tag].engine                  = RCAIDE.Analyses.Mission.Common.Conditions()
                fuel_line_results[pg_tag].rotor                   = RCAIDE.Analyses.Mission.Common.Conditions() 
                fuel_line_results[pg_tag].unique_rotor_tags       = sorted_propulsors.unique_rotor_tags
                fuel_line_results[pg_tag].unique_engine_tags      = sorted_propulsors.unique_engine_tags 
                fuel_line_results[pg_tag].y_axis_rotation         = 0. * ones_row(1)   # NEED TO REMOVE
                fuel_line_results[pg_tag].engine.efficiency       = 0. * ones_row(1)
                fuel_line_results[pg_tag].engine.torque           = 0. * ones_row(1) 
                fuel_line_results[pg_tag].engine.power            = 0. * ones_row(1) 
                fuel_line_results[pg_tag].engine.thottle          = 0. * ones_row(1) 
                fuel_line_results[pg_tag].rotor.torque            = 0. * ones_row(1)
                fuel_line_results[pg_tag].rotor.thrust            = 0. * ones_row(1)
                fuel_line_results[pg_tag].rotor.rpm               = 0. * ones_row(1)
                fuel_line_results[pg_tag].rotor.disc_loading      = 0. * ones_row(1)                 
                fuel_line_results[pg_tag].rotor.power_loading     = 0. * ones_row(1)
                fuel_line_results[pg_tag].rotor.tip_mach          = 0. * ones_row(1)
                fuel_line_results[pg_tag].rotor.efficiency        = 0. * ones_row(1)   
                fuel_line_results[pg_tag].rotor.figure_of_merit   = 0. * ones_row(1) 
                fuel_line_results[pg_tag].rotor.power_coefficient = 0. * ones_row(1)    
            
        # Ensure the mission knows how to pack and unpack the unknowns and residuals
        segment.process.iterate.unknowns.network                    = self.unpack_unknowns
        segment.process.iterate.residuals.network                   = self.residuals        
        return segment
            
    __call__ = evaluate_thrust
