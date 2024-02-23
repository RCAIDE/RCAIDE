## @ingroup Methods-Energy-Propulsion-Networks
# RCAIDE/Methods/Energy/Propulsion/Networks/internal_combustion_engine_propulsor.py
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
# internal_combustion_engine_propulsor
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsion-Networks
def internal_combustion_engine_propulsor(fuel_line,state): 
    ''' Computes the perfomrance of all internal combustion engine-propellers 
    connected to a fuel tank
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:   
    fuel_line            - data structure containing turbofans on distrubution network  [-]   
    state                - operating data structure                                     [-] 
                     
    Outputs:                      
    outputs              - ice_propeller operating outputs                              [-]
    total_thrust         - thrust of internal combustion engine propellers              [N]
    total_power          - power of internal combustion engine propellers               [W] 
    
    Properties Used: 
    N.A.        
    ''' 
    total_power     = 0*state.ones_row(1) 
    total_thrust    = 0*state.ones_row(3) 
    conditions      = state.conditions
    stored_results_flag  = False 
    
    for ice_propeller in fuel_line.propulsors:  
        if ice_propeller.active == True:   
            if fuel_line.identical_propulsors == False:
                # run analysis  
                total_thrust,total_power ,stored_results_flag,stored_propulsor_tag = compute_performance(conditions,fuel_line,ice_propeller,total_thrust,total_power)
            else:             
                if stored_results_flag == False: 
                    # run analysis 
                    total_thrust,total_power ,stored_results_flag,stored_propulsor_tag = compute_performance(conditions,fuel_line,ice_propeller,total_thrust,total_power)
                else:
                    # use old results 
                    total_thrust,total_power  = reuse_stored_data(conditions,fuel_line,ice_propeller,stored_propulsor_tag,total_thrust,total_power)
                
    return total_thrust,total_power 
    
def compute_performance(conditions,fuel_line,ice_propeller,total_thrust,total_power):  
    ''' Computes the perfomrance of one ice_propeller
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure        [-]  
    fuel_line            - fuelline                                   [-] 
    ice_propeller        - ice_propeller data structure               [-] 
    total_thrust         - thrust of ice_propeller group              [N]
    total_power          - power of ice_propeller group               [W] 

    Outputs:  
    total_thrust         - thrust of ice_propeller group              [N]
    total_power          - power of ice_propeller group               [W] 
    stored_results_flag  - boolean for stored results                 [-]     
    stored_propulsor_tag - name of ice_propeller with stored results  [-]
    
    Properties Used: 
    N.A.        
    '''  
    ice_results             = conditions.energy[fuel_line.tag][ice_propeller.tag]
    noise_results           = conditions.noise[fuel_line.tag][ice_propeller.tag] 
    engine                  = ice_propeller.engine 
    propeller               = ice_propeller.propeller
    eta                     = ice_results.throttle  
    RPM                     = ice_results.engine.rpm

    # Throttle the engine
    engine.inputs.speed    = RPM * Units.rpm   
    engine.calculate_power_out_from_throttle(conditions,eta)    
    torque                 = engine.outputs.torque     
    
    # link engine RPM to propeller 
    propeller.inputs.omega = RPM * Units.rpm 

    # Spin the propeller 
    F, Q, P, Cp, outputs, etap = propeller.spin(conditions) 

    # Check to see if magic thrust is needed, the ESC caps throttle at 1.1 already
    P[eta>1.0]          = P[eta>1.0]*eta[eta>1.0]
    F[eta[:,0]>1.0,:]   = F[eta[:,0]>1.0,:]*eta[eta[:,0]>1.0,:]

    # Determine Conditions specific to this instantation of engine and rotors
    R                   = propeller.tip_radius
    rpm                 = engine.inputs.speed / Units.rpm 
    F_mag               = np.atleast_2d(np.linalg.norm(F, axis=1)).T  

    # Create the outputs 
    ice_results.fuel_flow_rate            = engine.outputs.fuel_flow_rate
    ice_results.engine.power              = P 
    ice_results.engine.torque             = torque
    ice_results.throttle                  = eta 
    ice_results.rotor.torque              = Q
    ice_results.rotor.thrust              = F
    ice_results.rotor.rpm                 = rpm
    ice_results.rotor.tip_mach            = (R*rpm*Units.rpm)/conditions.freestream.speed_of_sound    
    ice_results.rotor.disc_loading        = (F_mag)/(np.pi*(R**2))             
    ice_results.rotor.power_loading       = (F_mag)/(P)    
    ice_results.rotor.efficiency          = etap
    ice_results.rotor.figure_of_merit     = outputs.figure_of_merit
    noise_results.rotor                   = outputs  
    total_power                           += P
    total_thrust                          += F  
    stored_results_flag                   = True
    stored_propulsor_tag                  = ice_propeller.tag  
 
    return total_thrust,total_power,stored_results_flag,stored_propulsor_tag
    
    
    
def reuse_stored_data(conditions,fuel_line,ice_propeller,stored_propulsor_tag,total_thrust,total_power):
    '''Reuses results from one ice_propeller for identical propulsors
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure        [-]  
    fuel_line            - fuel line                                  [-] 
    ice_propeller        - ice_propeller data structure               [-] 
    total_thrust         - thrust of ice_propeller group              [N]
    total_power          - power of ice_propeller group               [W] 

    Outputs:  
    total_thrust         - thrust of ice_propeller group              [N]
    total_power          - power of ice_propeller group               [W] 
    
    Properties Used: 
    N.A.        
    ''' 
    ice_results_0                         = conditions.energy[fuel_line.tag][stored_propulsor_tag]
    noise_results_0                       = conditions.noise[fuel_line.tag][stored_propulsor_tag] 
    ice_results                           = conditions.energy[fuel_line.tag][ice_propeller.tag]  
    noise_results                         = conditions.noise[fuel_line.tag][ice_propeller.tag]  
    ice_results.mass_flow_rate            = ice_results_0.mass_flow_rate          
    ice_results.engine.power              = ice_results_0.engine.power            
    ice_results.engine.torque             = ice_results_0.engine.torque           
    ice_results.throttle                  = ice_results_0.throttle         
    ice_results.rotor.torque              = ice_results_0.rotor.torque            
    ice_results.rotor.thrust              = ice_results_0.rotor.thrust            
    ice_results.rotor.rpm                 = ice_results_0.rotor.rpm               
    ice_results.rotor.tip_mach            = ice_results_0.rotor.tip_mach          
    ice_results.rotor.disc_loading        = ice_results_0.rotor.disc_loading      
    ice_results.rotor.power_loading       = ice_results_0.rotor.power_loading     
    ice_results.rotor.efficiency          = ice_results_0.rotor.efficiency        
    ice_results.rotor.figure_of_merit     = ice_results_0.rotor.figure_of_merit 
    ice_results.fuel_flow_rate            = ice_results_0.fuel_flow_rate 
    noise_results.rotor                   = noise_results_0.rotor      
    total_power                           += ice_results.engine.power
    total_thrust                          += ice_results.rotor.thrust 
    
    return total_thrust,total_power   

            
               