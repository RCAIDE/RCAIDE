## @ingroup Networks
# RCAIDE/Energy/Networks/Turbofan_Engine_Network.py
# 
#
# Created: Oct 2023, RCAIDE Team
# Modified:

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------------------------------------------------------
# RCAIDE Imports   
from RCAIDE.Framework.Mission.Common                                                           import Residuals , Conditions
from RCAIDE.Library.Methods.Propulsors.Turbofan_Propulsor.compute_turbofan_performance         import compute_turbofan_performance
from RCAIDE.Framework.Mission.Functions.Common.Unpack_Unknowns.energy import fuel_line_unknowns
from .Network                                                                                  import Network  

# ----------------------------------------------------------------------------------------------------------------------
#  Turbofan
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks
class Turbofan_Engine_Network(Network):
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
        
    # linking the different network components
    def evaluate(self,state,center_of_gravity):
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
                
                # Step 2.1: Compute and store perfomrance of all propulsors 
                fuel_line_T,fuel_line_M,fuel_line_P = compute_turbofan_performance(fuel_line,state,center_of_gravity)  
                total_thrust += fuel_line_T   
                total_moment += fuel_line_M   
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
        if reverse_thrust ==  True:
            total_thrust =  total_thrust* -1
            total_moment =  total_moment* -1
            
        conditions.energy.thrust_force_vector  = total_thrust
        conditions.energy.thrust_moment_vector = total_moment
        conditions.energy.power                = total_power 
        conditions.energy.vehicle_mass_rate    = total_mdot    
        
        return  
     
    
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
            segment   - data structure of mission segment [-]
        
        Outputs: 
        
        Properties Used:
        N/A
        """            
         
        fuel_lines = segment.analyses.energy.vehicle.networks.turbofan_engine.fuel_lines
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
        fuel_lines  = segment.analyses.energy.vehicle.networks.turbofan_engine.fuel_lines
        ones_row    = segment.state.ones_row 
        segment.state.residuals.network = Residuals()  
        
        for fuel_line_i, fuel_line in enumerate(fuel_lines):    
            # ------------------------------------------------------------------------------------------------------            
            # Create fuel_line results data structure  
            # ------------------------------------------------------------------------------------------------------
            segment.state.conditions.energy[fuel_line.tag]       =Conditions()       
            fuel_line_results                                    = segment.state.conditions.energy[fuel_line.tag]    
            segment.state.conditions.noise[fuel_line.tag]        = Conditions()  
            noise_conditions                                        = segment.state.conditions.noise[fuel_line.tag]      
     
            for fuel_tank in fuel_line.fuel_tanks:               
                fuel_line_results[fuel_tank.tag]                 = Conditions()  
                fuel_line_results[fuel_tank.tag].mass_flow_rate  = ones_row(1)  
                fuel_line_results[fuel_tank.tag].mass            = ones_row(1)  
                
            # ------------------------------------------------------------------------------------------------------
            # Assign network-specific  residuals, unknowns and results data structures
            # ------------------------------------------------------------------------------------------------------
            for turbofan in fuel_line.propulsors:
            
                ram                       = turbofan.ram
                inlet_nozzle              = turbofan.inlet_nozzle
                low_pressure_compressor   = turbofan.low_pressure_compressor
                high_pressure_compressor  = turbofan.high_pressure_compressor
                fan                       = turbofan.fan
                combustor                 = turbofan.combustor
                high_pressure_turbine     = turbofan.high_pressure_turbine
                low_pressure_turbine      = turbofan.low_pressure_turbine
                core_nozzle               = turbofan.core_nozzle
                fan_nozzle                = turbofan.fan_nozzle                 

                fuel_line_results[turbofan.tag]                                                = Conditions() 
                fuel_line_results[turbofan.tag].throttle                                       = 0. * ones_row(1)      
                fuel_line_results[turbofan.tag].y_axis_rotation                                = 0. * ones_row(1)  
                fuel_line_results[turbofan.tag].thrust                                         = 0. * ones_row(1) 
                fuel_line_results[turbofan.tag].power                                          = 0. * ones_row(1)
                fuel_line_results[turbofan.tag][combustor.tag]                        = Conditions() 
                fuel_line_results[turbofan.tag][combustor.tag].inputs                 = Conditions() 
                fuel_line_results[turbofan.tag][combustor.tag].inputs.nondim_mass_ratio  = ones_row(1)
                fuel_line_results[turbofan.tag][combustor.tag].outputs                = Conditions()
                fuel_line_results[turbofan.tag][ram.tag]                              = Conditions() 
                fuel_line_results[turbofan.tag][ram.tag].inputs                       = Conditions() 
                fuel_line_results[turbofan.tag][ram.tag].outputs                      = Conditions() 
                fuel_line_results[turbofan.tag][fan.tag]                              = Conditions() 
                fuel_line_results[turbofan.tag][fan.tag].inputs                       = Conditions() 
                fuel_line_results[turbofan.tag][fan.tag].outputs                      = Conditions() 
                fuel_line_results[turbofan.tag][high_pressure_compressor.tag]         = Conditions()
                fuel_line_results[turbofan.tag][high_pressure_compressor.tag].inputs  = Conditions()
                fuel_line_results[turbofan.tag][high_pressure_compressor.tag].outputs = Conditions()
                fuel_line_results[turbofan.tag][low_pressure_compressor.tag]          = Conditions()
                fuel_line_results[turbofan.tag][low_pressure_compressor.tag].inputs   = Conditions()
                fuel_line_results[turbofan.tag][low_pressure_compressor.tag].outputs  = Conditions()
                fuel_line_results[turbofan.tag][high_pressure_turbine.tag]            = Conditions()
                fuel_line_results[turbofan.tag][high_pressure_turbine.tag].inputs     = Conditions()
                fuel_line_results[turbofan.tag][high_pressure_turbine.tag].outputs    = Conditions()
                fuel_line_results[turbofan.tag][low_pressure_turbine.tag]             = Conditions()
                fuel_line_results[turbofan.tag][low_pressure_turbine.tag].inputs      = Conditions()
                fuel_line_results[turbofan.tag][low_pressure_turbine.tag].outputs     = Conditions()
                fuel_line_results[turbofan.tag][core_nozzle.tag]                      = Conditions()
                fuel_line_results[turbofan.tag][core_nozzle.tag].inputs               = Conditions()
                fuel_line_results[turbofan.tag][core_nozzle.tag].outputs              = Conditions()
                fuel_line_results[turbofan.tag][fan_nozzle.tag]                       = Conditions()
                fuel_line_results[turbofan.tag][fan_nozzle.tag].inputs                = Conditions()
                fuel_line_results[turbofan.tag][fan_nozzle.tag].outputs               = Conditions()
                fuel_line_results[turbofan.tag][inlet_nozzle.tag]                     = Conditions()
                fuel_line_results[turbofan.tag][inlet_nozzle.tag].inputs              = Conditions()
                fuel_line_results[turbofan.tag][inlet_nozzle.tag].outputs             = Conditions()
                fuel_line_results[turbofan.tag].inputs                                         = Conditions()
                fuel_line_results[turbofan.tag].outputs                                        = Conditions() 
                
                noise_conditions[turbofan.tag]                             = Conditions() 
                noise_conditions[turbofan.tag].turbofan                    = Conditions() 
        
        segment.process.iterate.unknowns.network   = self.unpack_unknowns                   
        return segment    
        
    __call__ = evaluate 
