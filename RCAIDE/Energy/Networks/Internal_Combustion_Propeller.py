# RCAIDE/Energy/Networks/Internal_Combustion_Propeller.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports 
import RCAIDE 
from RCAIDE.Core                                                    import Data 
from RCAIDE.Analyses.Mission.Segments.Conditions                    import Residuals 
from RCAIDE.Components.Component                                    import Container    
from RCAIDE.Methods.Propulsion.internal_combustion_engine_propulsor import compute_propulsor_performance ,compute_unique_propulsor_groups 
from .Network                                                       import Network   

# ----------------------------------------------------------------------------------------------------------------------
#  Internal_Combustion_Propeller
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks
class Internal_Combustion_Propeller(Network):
    """ A simple mock up of an internal combustion propeller engine.  
        Electronic speed controllers, thermal management system, avionics, and other eletric 
        power systes paylaods are also modelled. Rotors and motors are arranged into groups,
        called propulsor groups, to siginify how they are connected in the network.  
        This network adds additional unknowns and residuals to the mission to determinge 
        the torque matching between motors and rotors in each propulsor group.  
    
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
        self.engines                      = Container()
        self.propellers                   = Container()   
        self.active_propulsor_groups      = None  
    
    # manage process with a driver function
    def evaluate_thrust(self,state):
        """ Calculate thrust given the current state of the vehicle
    
            Assumptions:
    
            Source:
            N/A
    
            Inputs:
            state [state()]
    
            Outputs:
            results.thrust_force_vector [newtons]
            results.vehicle_mass_rate   [kg/s]
            conditions.energy:
                rpm                  [radians/sec]
                propeller.torque     [N-M]
                power                [W]
    
            Properties Used:
            Defaulted values
        """           
        # unpack
        conditions   = state.conditions
        engines      = self.engines
        propellers   = self.propellers    
     
        total_mdot   = 0.
        total_thrust = 0. * state.ones_row(3)
        total_power  = 0. 
 
        for i in range(state.conditions.energy[self.tag].number_of_propulsor_groups):
            if self.active_propulsor_groups[i]:           
                pg_tag                 = state.conditions.energy[self.tag].active_propulsor_groups[i]
                N_rotors               = state.conditions.energy[self.tag].N_rotors
                outputs , T , P, mdot  = compute_propulsor_performance(i,self.tag,pg_tag,engines,propellers,N_rotors,state)  
                total_mdot             += mdot
                total_thrust           += T       
                total_power            += P    
                 
        # Create the outputs
        conditions.energy.power = total_power
        
        results = Data()
        results.thrust_force_vector       = total_thrust
        results.vehicle_mass_rate         = mdot 
        
        return results
    
    
    def unpack_unknowns(self,segment):
        """Unpacks the unknowns set in the mission to be available for the mission.

        Assumptions:
        N/A
        
        Source:
        N/A
        
        Inputs:
        state.unknowns.rpm                 [RPM] 
        
        Outputs:
        state.conditions.energy.rpm    [RPM] 

        
        Properties Used:
        N/A
        """            

        for i in range(segment.state.conditions.energy.number_of_propulsor_groups):  
            ICE_net_results         = segment.state.conditions.energy[self.tag] 
            active_propulsor_groups = ICE_net_results.active_propulsor_groups
            for i in range(len(active_propulsor_groups)):             
                    pg_tag = active_propulsor_groups[i]         
                    ICE_net_results[pg_tag].rotor.power_coefficient = segment.state.unknowns[self.tag + '_' + pg_tag + '_rpm']  
        
        return
    
    def residuals(self,segment):
        """ Calculates a residual based on torques 
        
        Assumptions:
        
        Inputs:
            segment.state.conditions.energy.
                engine.torque                       [newtom-meters]                 
                propeller.torque                   [newtom-meters] 
        
        Outputs:
            segment.state:
                residuals.network                  [newtom-meters] 
                
        Properties Used:
            N/A
                                
        """     
        ICE_net_results         = segment.state.conditions.energy[self.tag] 
        active_propulsor_groups = ICE_net_results.active_propulsor_groups
        for i in range(len(active_propulsor_groups)): 
            q_motor   = ICE_net_results[active_propulsor_groups[i]].engine.torque
            q_prop    = ICE_net_results[active_propulsor_groups[i]].rotor.torque 
            segment.state.residuals.network[self.tag + '_' + active_propulsor_groups[i] + '_rotor_motor_torque'] = q_motor - q_prop 
        
        return
    
    def add_unknowns_and_residuals_to_segment(self, segment,rpms=[2500]):
        """ This function sets up the information that the mission needs to run a mission segment using this network
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            segment
            rpm                                                                   [rpm]
            
            Outputs:
            segment.state.unknowns.battery_voltage_under_load
            segment.state.unknowns.propeller_power_coefficient 
    
            Properties Used:
            N/A
        """                  
        ones_row = segment.state.ones_row 
        segment.state.residuals.network = Residuals() 
        
        if 'throttle' in segment.state.unknowns: 
            segment.state.unknowns.pop('throttle')
        if 'throttle' in segment.state.conditions.energy: 
            segment.state.conditions.energy.pop('throttle')
          
        active_propulsor_groups   = self.active_propulsor_groups 
        N_active_propulsor_groups = len(active_propulsor_groups) 

        # ------------------------------------------------------------------------------------------------------            
        # Create bus results data structure  
        # ------------------------------------------------------------------------------------------------------
        segment.state.conditions.energy[self.tag] = RCAIDE.Analyses.Mission.Segments.Conditions.Conditions()            

        # ------------------------------------------------------------------------------------------------------            
        # Determine number of propulsor groups in bus
        # ------------------------------------------------------------------------------------------------------
        sorted_propulsors                       = compute_unique_propulsor_groups(self)
        bus_results                             = segment.state.conditions.energy[self.tag]
        bus_results.number_of_propulsor_groups  = N_active_propulsor_groups
        bus_results.active_propulsor_groups     = active_propulsor_groups
        bus_results.N_rotors                    = sorted_propulsors.N_rotors 
            
        # ------------------------------------------------------------------------------------------------------
        # Assign network-specific  residuals, unknowns and results data structures
        # ------------------------------------------------------------------------------------------------------
        for i in range(len(sorted_propulsors.unique_rotor_tags)):    
            segment.state.residuals[self.tag + '_' + active_propulsor_groups[i]]           =  0. * ones_row(1)  
            segment.state.unknowns[self.tag + '_' + active_propulsor_groups[i] + '_rpm']   = rpms[i] * ones_row(1)  
                         
            # Results data structure for each propulsor group    
            pg_tag                                      = active_propulsor_groups[i] 
            bus_results[pg_tag]                         = RCAIDE.Analyses.Mission.Segments.Conditions.Conditions()
            bus_results[pg_tag].engine                  = RCAIDE.Analyses.Mission.Segments.Conditions.Conditions()
            bus_results[pg_tag].rotor                   = RCAIDE.Analyses.Mission.Segments.Conditions.Conditions() 
            bus_results[pg_tag].unique_rotor_tags       = sorted_propulsors.unique_rotor_tags
            bus_results[pg_tag].unique_engine_tags      = sorted_propulsors.unique_motor_tags 
            bus_results[pg_tag].throttle                = 0. * ones_row(1)     
            bus_results[pg_tag].engine.torque           = 0. * ones_row(1) 
            bus_results[pg_tag].rotor.torque            = 0. * ones_row(1)
            bus_results[pg_tag].rotor.thrust            = 0. * ones_row(1)
            bus_results[pg_tag].rotor.rpm               = 0. * ones_row(1)
            bus_results[pg_tag].rotor.disc_loading      = 0. * ones_row(1)                 
            bus_results[pg_tag].rotor.power_loading     = 0. * ones_row(1)
            bus_results[pg_tag].rotor.tip_mach          = 0. * ones_row(1)
            bus_results[pg_tag].rotor.efficiency        = 0. * ones_row(1)   
            bus_results[pg_tag].rotor.figure_of_merit   = 0. * ones_row(1) 
            bus_results[pg_tag].rotor.power_coefficient = 0. * ones_row(1)    
                 
        # Ensure the mission knows how to pack and unpack the unknowns and residuals
        segment.process.iterate.unknowns.network                    = self.unpack_unknowns
        segment.process.iterate.residuals.network                   = self.residuals        

        return segment
            
    __call__ = evaluate_thrust
