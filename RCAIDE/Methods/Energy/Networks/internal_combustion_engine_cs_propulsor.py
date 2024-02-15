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
def internal_combustion_engine_cs_propulsor(fuel_line,state): 
    ''' Computes the perfomrance of all constant-speed internal combustion engine-propellers 
    connected to a fuel tank
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:   
    fuel_line            - data structure containing turbofans on distrubution network  [-]   
    state                - operating data structure                                     [-] 
                     
    Outputs:                      
    outputs              - ice_propeller operating outputs                                  [-]
    total_thrust         - thrust of internal combustion engine propellers              [N]
    total_power          - power of internal combustion engine propellers               [W]
    total_mdot           - mass flow rate of fuel                                       [kg/s]
    
    Properties Used: 
    N.A.        
    '''

    total_mdot      = 0*state.ones_row(1) 
    total_power     = 0*state.ones_row(1) 
    total_thrust    = 0*state.ones_row(3) 
    conditions      = state.conditions
    stored_results_flag  = False 
     
    for ice_propeller in fuel_line.propulsors:  
        if ice_propeller.active == True:  
            if fuel_line.identical_propulsors == False:
                # run analysis  
                total_thrust,total_power,total_mdot ,stored_results_flag,stored_propulsor_tag = compute_performance(conditions,fuel_line,ice_propeller,total_thrust,total_power,total_mdot)
            else:             
                if stored_results_flag == False: 
                    # run analysis 
                    total_thrust,total_power,total_mdot ,stored_results_flag,stored_propulsor_tag = compute_performance(conditions,fuel_line,ice_propeller,total_thrust,total_power,total_mdot)
                else:
                    # use old results 
                    total_thrust,total_power,total_mdot  = reuse_stored_data(conditions,fuel_line,ice_propeller,stored_propulsor_tag,total_thrust,total_power,total_mdot)
                
    return total_thrust,total_power,total_mdot 
    
def compute_performance(conditions,fuel_line,ice_propeller,total_thrust,total_power,total_mdot):  
    ''' Computes the perfomrance of one ice_propeller
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure    [-]  
    fuel_line            - fuelline                               [-] 
    ice_propeller        - ice_propeller data structure               [-] 
    total_thrust         - thrust of ice_propeller group              [N]
    total_power          - power of ice_propeller group               [W]
    total_mdot           - mass flow rate of ice_propeller group      [kg/s]

    Outputs:  
    total_thrust         - thrust of ice_propeller group              [N]
    total_power          - power of ice_propeller group               [W]
    total_mdot           - mass flow rate of ice_propeller group      [kg/s]
    stored_results_flag  - boolean for stored results             [-]     
    stored_propulsor_tag - name of ice_propeller with stored results  [-]
    
    Properties Used: 
    N.A.        
    '''  
    ice_cs_results          = conditions.energy[fuel_line.tag][ice_propeller.tag]
    noise_results           = conditions.noise[fuel_line.tag][ice_propeller.tag] 
    engine                  = ice_propeller.engine 
    rotor                   = ice_propeller.rotor 

    ## Run the rotor to get the power
    #rotor.inputs.pitch_command = ice_cs_results.rotor.pitch_command
    #rotor.inputs.omega         = ice_cs_results.engine.rpm

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
    ice_cs_results.fuel_flow_rate        = engine.outputs.fuel_flow_rate 
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
    total_mdot                           += ice_cs_results.fuel_flow_rate   
    stored_results_flag                  = True
    stored_propulsor_tag                 = ice_propeller.tag   
    
 
    return total_thrust,total_power,total_mdot ,stored_results_flag,stored_propulsor_tag 
    
def reuse_stored_data(conditions,fuel_line,ice_propeller,stored_propulsor_tag,total_thrust,total_power,total_mdot):
    '''Reuses results from one ice_propeller for identical propulsors
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure    [-]  
    fuel_line            - fuel_line                              [-] 
    ice_propeller        - ice_propeller data structure           [-] 
    total_thrust         - thrust of ice_propeller group          [N]
    total_power          - power of ice_propeller group           [W]
    total_mdot           - mass flow rate of ice_propeller group  [kg/s]

    Outputs:  
    total_thrust         - thrust of ice_propeller group          [N]
    total_power          - power of ice_propeller group           [W]
    total_mdot           - mass flow rate of ice_propeller group  [kg/s]
    
    Properties Used: 
    N.A.        
    ''' 
    ice_cs_results_0                         = conditions.energy[fuel_line.tag][stored_propulsor_tag]
    noise_results_0                          = conditions.noise[fuel_line.tag][stored_propulsor_tag] 
    ice_cs_results                           = conditions.energy[fuel_line.tag][ice_propeller.tag]  
    noise_results                            = conditions.noise[fuel_line.tag][ice_propeller.tag]  
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
    total_mdot                               += ice_cs_results_0.fuel_flow_rate 
    total_power                              += ice_cs_results.engine.power
    total_thrust                             += ice_cs_results.rotor.thrust 
 
    return total_thrust,total_power,total_mdot 
 