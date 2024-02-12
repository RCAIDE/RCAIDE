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
from RCAIDE.Core                                                      import Data 
from RCAIDE.Analyses.Mission.Common                                   import Residuals    
from RCAIDE.Methods.Energy.Networks.turbofan_propulsor                import turbofan_propulsor
from .Network                                                         import Network  

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
                fuel_line_T,fuel_line_P = turbofan_propulsor(fuel_line,state)  
                total_thrust += fuel_line_T   
                total_power  += fuel_line_P  
                
                # Step 2.2: Link each propulsor the its respective fuel tank(s)
                for fuel_tank in fuel_line.fuel_tanks:
                    mdot = 0. * state.ones_row(1)   
                    for propulsor in fuel_line.propulsors:
                        for source in (propulsor.energy_sources):
                            if fuel_tank.tag == source: 
                                mdot += conditions.energy[fuel_line.tag][propulsor.tag].fuel_flow_rate 
                        
                    # Step 2.3 : Determine cumulative fuel flow from fuel tank 
                    fuel_tank_mdot = fuel_tank.fuel_selector_ratio*mdot + fuel_tank.secondary_fuel_flow 
                    
                    # Step 2.4: Store mass flow results 
                    conditions.energy[fuel_line.tag][fuel_tank.tag].mass_flow_rate  = fuel_tank_mdot  
                    total_mdot += fuel_tank_mdot                    
                            
        # Step 3: Pack results 
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
            segment   - data structure of mission segment [-]
        
        Outputs: 
        
        Properties Used:
        N/A
        """            
        

        ones_row   = segment.state.ones_row  
        fuel_lines = segment.analyses.energy.networks.turbofan_engine.fuel_lines
        
        # Body Angle Control
        if segment.body_angle_control.active:
            segment.state.unknowns.body_angle   
            segment.state.conditions.frames.body.inertial_rotations[:,1] = segment.state.unknowns.body_angle[:,0]    
            
                
        ## Wing Angle Control
        #if segment.wind_angle_control.active:
            #segment.state.unknowns.wind_angle            
            
        # Throttle Control
        if segment.throttle_control.active:
            for fuel_line in fuel_lines:
                fuel_line_results   = segment.state.conditions.energy[fuel_line.tag]    
                num_throttles      = len(segment.throttle_control.assigned_propulsors)   
                for i in range(num_throttles):
                    for j in range(len(segment.throttle_control.assigned_propulsors[i])): 
                        propulsor_name = segment.throttle_control.assigned_propulsors[i][j]
                        fuel_line_results[propulsor_name].throttle = segment.state.unknowns["throttle_" + str(i)] 
                     
        ## Elevator Control
        #if segment.elevator_deflection_control.active: 
            #num_elev_ctrls = len(segment.elevator_deflection_control.assigned_propulsors) 
            #for i in range(num_elev_ctrls):   
                #segment.state.unknowns["elevator_control_" + str(i)]    
                    
        ## Flap Control
        #if segment.flap_deflection_control.active: 
            #num_flap_ctrls = len(segment.flap_deflection_control.assigned_propulsors) 
            #for i in range(num_flap_ctrls):   
                #segment.state.unknowns["flap_control_" + str(i)]       
                
        ## Aileron Control
        #if segment.aileron_deflection_control.active: 
            #num_aile_ctrls = len(segment.aileron_deflection_control.assigned_propulsors) 
            #for i in range(num_aile_ctrls):   
                #segment.state.unknowns["aileron_control_" + str(i)]       
            
        ## Thrust Control
        #if segment.thrust_vector_angle_control.active: 
            #num_tv_ctrls = len(segment.thrust_vector_angle_control.assigned_propulsors) 
            #for i in range(num_tv_ctrls):   
                #segment.state.unknowns["thrust_control_" + str(i)]      
            
        ## Blade Pitch Control
        #if segment.blade_pitch_angle_control.active: 
            #num_bpa_ctrls = len(segment.blade_pitch_angle_control.assigned_propulsors) 
            #for i in range(num_bpa_ctrls):   
                #segment.state.unknowns["blade_pitch_angle_" + str(i)]       
                                                                                      
        ## RPM Control
        #if segment.RPM_control.active: 
            #num_rpm_ctrls = len(segment.RPM_control.assigned_propulsors) 
            #for i in range(num_rpm_ctrls):   
                #segment.state.unknowns["rpm_control_" + str(i)]        
        
        
                

        #fuel_lines   = segment.analyses.energy.networks.turbofan_engine.fuel_lines  
        #for fuel_line_i, fuel_line in enumerate(fuel_lines):            
            #if (type(segment) == RCAIDE.Analyses.Mission.Segments.Ground.Takeoff):
                #pass
            #elif (type(segment) == RCAIDE.Analyses.Mission.Segments.Ground.Landing):   
                #pass
            #elif (type(segment) == RCAIDE.Analyses.Mission.Segments.Cruise.Constant_Throttle_Constant_Altitude) \
                 #or (type(segment) == RCAIDE.Analyses.Mission.Segments.Single_Point.Set_Speed_Set_Throttle)\
                 #or (type(segment) == RCAIDE.Analyses.Mission.Segments.Climb.Constant_Throttle_Constant_Speed):
                #pass    
            #elif fuel_line.active:    
                #fuel_line_results           = segment.state.conditions.energy[fuel_line.tag]  
                #fuel_line_results.throttle  = segment.state.unknowns[fuel_line.tag + '_throttle']  
        
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
        fuel_lines  = segment.analyses.energy.networks.turbofan_engine.fuel_lines
        ones_row    = segment.state.ones_row 
        segment.state.residuals.network = Residuals()  
        
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
            elif (type(segment) == RCAIDE.Analyses.Mission.Segments.Cruise.Constant_Throttle_Constant_Altitude)\
                 or (type(segment) == RCAIDE.Analyses.Mission.Segments.Single_Point.Set_Speed_Set_Throttle)\
                 or (type(segment) == RCAIDE.Analyses.Mission.Segments.Climb.Constant_Throttle_Constant_Speed):
                fuel_line_results.throttle = segment.throttle * ones_row(1)            
     
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
