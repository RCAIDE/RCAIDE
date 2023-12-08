## @ingroup Energy-Networks
# RCAIDE/Energy/Networks/Internal_Combustion_Engine.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports 
import RCAIDE 
from RCAIDE.Core                                                    import Data 
from RCAIDE.Analyses.Mission.Common                                 import Residuals    
from RCAIDE.Methods.Propulsion.Performance.internal_combustion_engine_propulsor import internal_combustion_engine_propulsor
from .Network                                                       import Network   

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
        
        #Unpack
        conditions  = state.conditions 
        fuel_lines  = self.fuel_lines 
    
        total_thrust  = 0. * state.ones_row(3) 
        total_power   = 0. * state.ones_row(1) 
        total_mdot    = 0. * state.ones_row(1) 
    
        for fuel_line in fuel_lines:  
            if fuel_line.active:             
                fuel_tanks   = fuel_line.fuel_tanks    
                fuel_line_T , fuel_line_P, fuel_line_mdot  = internal_combustion_engine_propulsor(fuel_line,state)    
        
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
            if fuel_line.active: 
                fuel_line_results           = segment.state.conditions.energy[fuel_line.tag]  
                fuel_line_results.throttle  = segment.state.unknowns[fuel_line.tag + '_throttle']  
                for propulsor in fuel_line.propulsors: 
                    fuel_line_results[propulsor.tag].rotor.rpm = segment.state.unknowns[fuel_line.tag + '_' + propulsor.tag + '_rpm']   
        
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
            for propulsor in fuel_line.propulsors: 
                q_engine   = fuel_line_results[propulsor.tag].engine.torque
                q_prop    = fuel_line_results[propulsor.tag].rotor.torque 
                segment.state.residuals.network[fuel_line.tag + '_' + propulsor.tag + '_rotor_engine_torque'] = q_engine - q_prop 
        
        return
    
    def add_unknowns_and_residuals_to_segment(self,
                                              segment,
                                              estimated_throttles = [[0.5]], 
                                              estimated_rpms      = [[2500]]):
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
        
        fuel_lines  = segment.analyses.energy.networks.internal_combustion_engine.fuel_lines
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
            segment.state.conditions.noise[fuel_line.tag]        = RCAIDE.Analyses.Mission.Common.Conditions()  
            noise_results                                        = segment.state.conditions.noise[fuel_line.tag]

            if (type(segment) == RCAIDE.Analyses.Mission.Segments.Ground.Takeoff):
                pass
            elif (type(segment) == RCAIDE.Analyses.Mission.Segments.Ground.Landing):   
                pass 
            elif (type(segment) == RCAIDE.Analyses.Mission.Segments.Cruise.Constant_Throttle_Constant_Altitude) or (type(segment) == RCAIDE.Analyses.Mission.Segments.Single_Point.Set_Speed_Set_Throttle):
                fuel_line_results.throttle = segment.throttle * ones_row(1)            
            elif fuel_line.active:    
                segment.state.unknowns[fuel_line.tag + '_throttle']  = estimated_throttles[fuel_line_i][0] * ones_row(1) 
 
            for fuel_tank in fuel_line.fuel_tanks:               
                fuel_line_results[fuel_tank.tag]                 = RCAIDE.Analyses.Mission.Common.Conditions()  
                fuel_line_results[fuel_tank.tag].mass_flow_rate  = ones_row(1)  
                fuel_line_results[fuel_tank.tag].mass            = ones_row(1)  
                
            # ------------------------------------------------------------------------------------------------------
            # Assign network-specific  residuals, unknowns and results data structures
            # ------------------------------------------------------------------------------------------------------
            for propulsor in fuel_line.propulsors:         

                segment.state.unknowns[fuel_line.tag + '_' + propulsor.tag + '_rpm']                           = estimated_rpms[fuel_line_i][0] * ones_row(1)  
                segment.state.residuals.network[ fuel_line.tag + '_' + propulsor.tag + '_rotor_engine_torque'] = 0. * ones_row(1)       
                
                fuel_line_results[propulsor.tag]                         = RCAIDE.Analyses.Mission.Common.Conditions()
                fuel_line_results[propulsor.tag].engine                  = RCAIDE.Analyses.Mission.Common.Conditions()
                fuel_line_results[propulsor.tag].rotor                   = RCAIDE.Analyses.Mission.Common.Conditions()  
                fuel_line_results[propulsor.tag].y_axis_rotation         = 0. * ones_row(1)   # NEED TO REMOVE
                fuel_line_results[propulsor.tag].engine.efficiency       = 0. * ones_row(1)
                fuel_line_results[propulsor.tag].engine.torque           = 0. * ones_row(1) 
                fuel_line_results[propulsor.tag].engine.power            = 0. * ones_row(1) 
                fuel_line_results[propulsor.tag].engine.throttle         = 0. * ones_row(1) 
                fuel_line_results[propulsor.tag].rotor.torque            = 0. * ones_row(1)
                fuel_line_results[propulsor.tag].rotor.thrust            = 0. * ones_row(1)
                fuel_line_results[propulsor.tag].rotor.rpm               = 0. * ones_row(1)
                fuel_line_results[propulsor.tag].rotor.disc_loading      = 0. * ones_row(1)                 
                fuel_line_results[propulsor.tag].rotor.power_loading     = 0. * ones_row(1)
                fuel_line_results[propulsor.tag].rotor.tip_mach          = 0. * ones_row(1)
                fuel_line_results[propulsor.tag].rotor.efficiency        = 0. * ones_row(1)   
                fuel_line_results[propulsor.tag].rotor.figure_of_merit   = 0. * ones_row(1) 
                fuel_line_results[propulsor.tag].rotor.power_coefficient = 0. * ones_row(1)    
                noise_results[propulsor.tag]                             = RCAIDE.Analyses.Mission.Common.Conditions()          
            
        # Ensure the mission knows how to pack and unpack the unknowns and residuals
        segment.process.iterate.unknowns.network                    = self.unpack_unknowns
        segment.process.iterate.residuals.network                   = self.residuals        
        return segment
            
    __call__ = evaluate_thrust
