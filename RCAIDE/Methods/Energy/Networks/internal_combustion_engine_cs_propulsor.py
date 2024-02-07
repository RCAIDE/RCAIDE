## @ingroup Methods-Energy-Propulsion-Networks
# RCAIDE/Methods/Energy/Propulsion/Networks/internal_combustion_engine_cs_propulsor.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Units  

# pacakge imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# internal_combustion_engine_constant_speed_propulsor
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsion-Networks
def internal_combustion_engine_cs_propulsor(fuel_line,assigned_propulsors,state): 
    ''' Computes the performance of an internal combustion engine propulsor constant speed unit
     
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    fuel_line             - distrubution component class              [string] 
    assigned_propulsors   - list of propulsors that are powered by energy source        [-]
    state                 - operating data structure                  [-] 
     
    Outputs:       
    total_thrust         - thrust of fuel line                        [N]
    total_power          - power of fuel line                         [W]
    total_mdot           - mass flow rate of fuel line                [kg/s]
    
    Properties Used: 
    N.A.            
    '''  

    total_mdot      = 0*state.ones_row(1) 
    total_power     = 0*state.ones_row(1) 
    total_thrust    = 0*state.ones_row(3) 
    conditions      = state.conditions
    stored_results = False 
    
    for i in range(len(assigned_propulsors)):
        propulsor = fuel_line.propulsors[assigned_propulsors[i]]  
        if propulsor.active == True: 
            if fuel_line.identical_propulsors == True and stored_results == False:
                fuel_line_results       = conditions.energy[fuel_line.tag]
                ice_cs_results          = fuel_line_results[propulsor.tag]
                noise_results           = conditions.noise[fuel_line.tag][propulsor.tag] 
                engine                  = propulsor.engine 
                rotor                   = propulsor.rotor 
            
                # Run the rotor to get the power
                rotor.inputs.pitch_command = ice_cs_results.rotor.pitch_command
                rotor.inputs.omega         = ice_cs_results.engine.rpm
            
                # Spin the rotor 
                F, Q, P, Cp, outputs, etap = rotor.spin(conditions) 
            
                # Run the engine to calculate the throttle setting and the fuel burn
                engine.inputs.power = P
                engine.calculate_throttle_out_from_power(conditions)
            
                # Create the outputs 
                R                   = rotor.tip_radius   
                rpm                 = engine.inputs.speed / Units.rpm 
                F_mag               = np.atleast_2d(np.linalg.norm(F, axis=1)).T
                throttle            = engine.outputs.throttle   
            
                # Pack specific outputs
                fuel_line_results.fuel_flow_rate     = engine.outputs.fuel_flow_rate 
                ice_cs_results.engine.torque         = Q
                ice_cs_results.engine.power          = P   
                ice_cs_results.engine.throttle       = throttle
                ice_cs_results.rotor.torque          = Q
                ice_cs_results.rotor.rpm             = rpm
                ice_cs_results.rotor.tip_mach        = (R*rpm*Units.rpm)/conditions.freestream.speed_of_sound 
                ice_cs_results.rotor.disc_loading    = (F_mag)/(np.pi*(R**2))             
                ice_cs_results.rotor.power_loading   = (F_mag)/(P)    
                ice_cs_results.rotor.efficiency      = etap
                ice_cs_results.rotor.figure_of_merit = outputs.figure_of_merit
                noise_results.rotor                  = outputs  
                total_power                          += P
                total_thrust                         += F 
                total_mdot                           += fuel_line_results.fuel_flow_rate   
                stored_results                       = True
                stored_propulsor_tag                 = propulsor.tag                      
            else:  
                ice_cs_results_0                         = conditions.energy[fuel_line.tag][fuel_line.propulsors[stored_propulsor_tag]]
                noise_results_0                          = conditions.noise[fuel_line.tag][fuel_line.propulsors[stored_propulsor_tag]]  
                ice_cs_results                           = conditions.energy[fuel_line.tag][propulsor.tag]   
                noise_results                            = conditions.noise[fuel_line.tag][propulsor.tag] 
                ice_cs_results.mass_flow_rate            = ice_cs_results_0.mass_flow_rate          
                ice_cs_results.engine.power              = ice_cs_results_0.engine.power            
                ice_cs_results.engine.torque             = ice_cs_results_0.engine.torque           
                ice_cs_results.engine.throttle           = ice_cs_results_0.engine.throttle         
                ice_cs_results.rotor.torque              = ice_cs_results_0.rotor.torque            
                ice_cs_results.rotor.thrust              = ice_cs_results_0.rotor.thrust            
                ice_cs_results.rotor.rpm                 = ice_cs_results_0.rotor.rpm               
                ice_cs_results.rotor.tip_mach            = ice_cs_results_0.rotor.tip_mach          
                ice_cs_results.rotor.disc_loading        = ice_cs_results_0.rotor.disc_loading      
                ice_cs_results.rotor.power_loading       = ice_cs_results_0.rotor.power_loading     
                ice_cs_results.rotor.efficiency          = ice_cs_results_0.rotor.efficiency        
                ice_cs_results.rotor.figure_of_merit     = ice_cs_results_0.rotor.figure_of_merit   
                noise_results.rotor                      = noise_results_0.rotor   
                total_mdot                               += fuel_line_results.fuel_flow_rate 
                total_power                              += ice_cs_results.engine.power
                total_thrust                             += ice_cs_results.rotor.thrust 
 
    return   total_thrust , total_power ,total_mdot
 