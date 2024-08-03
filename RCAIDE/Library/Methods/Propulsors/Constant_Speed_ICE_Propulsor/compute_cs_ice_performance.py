## @ingroup Methods-Energy-Propulsors-Constant_Speed_ICE_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Constant_Speed_ICE_Propulsor/compute_cs_ice_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Framework.Core import Units  
from RCAIDE.Library.Methods.Propulsors.Converters.Engine import compute_throttle_from_power

# pacakge imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# internal_combustion_engine_constant_speed_propulsor
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsors-Networks
def compute_cs_ice_performance(ice_cs_propeller,state,fuel_line,center_of_gravity= [[0.0, 0.0,0.0]]):  
    ''' Computes the perfomrance of one ice_cs_propeller
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure           [-]  
    fuel_line            - fuelline                                      [-] 
    ice_cs_propeller        - ice_cs_propeller data structure            [-] 
    total_thrust         - thrust of ice_cs_propeller group              [N]
    total_power          - power of ice_cs_propeller group               [W] 

    Outputs:  
    total_thrust         - thrust of ice_cs_propeller group              [N]
    total_power          - power of ice_cs_propeller group               [W] 
    stored_results_flag  - boolean for stored results                    [-]     
    stored_propulsor_tag - name of ice_cs_propeller with stored results  [-]
    
    Properties Used: 
    N.A.        
    '''  
    conditions              = state.conditions  
    ice_cs_conditions       = conditions.energy[fuel_line.tag][ice_cs_propeller.tag]
    noise_conditions        = conditions.noise[fuel_line.tag][ice_cs_propeller.tag] 
    engine                  = ice_cs_propeller.engine 
    propeller               = ice_cs_propeller.propeller
    RPM                     = ice_cs_conditions.engine.rpm  

    # Run the propeller to get the power
    ice_cs_conditions.rotor.inputs.inputs.omega    = RPM * Units.rpm
    ice_cs_conditions.rotor.inputs.pitch_command   = ice_cs_conditions.throttle - 0.5
    F, Q, P, Cp, outputs, etap       = propeller.spin(conditions) 

    # Run the engine to calculate the throttle setting and the fuel burn
    ice_cs_conditions.engine.inputs.power = P
    compute_throttle_from_power(engine,conditions)

    # Create the outputs 
    R                   = propeller.tip_radius    
    F_mag               = np.atleast_2d(np.linalg.norm(F, axis=1)).T
    throttle            = ice_cs_conditions.engine.outputs.throttle   

    # Pack specific outputs
    ice_cs_conditions.throttle              = throttle
    ice_cs_conditions.fuel_flow_rate        = ice_cs_conditions.engine.outputs.fuel_flow_rate 
    ice_cs_conditions.engine.torque         = Q
    ice_cs_conditions.engine.power          = P   
    ice_cs_conditions.rotor.torque          = Q
    ice_cs_conditions.rotor.rpm             = RPM 
    ice_cs_conditions.rotor.tip_mach        = (R*RPM *Units.rpm)/conditions.freestream.speed_of_sound 
    ice_cs_conditions.rotor.disc_loading    = (F_mag)/(np.pi*(R**2))             
    ice_cs_conditions.rotor.power_loading   = (F_mag)/(P)    
    ice_cs_conditions.rotor.efficiency      = etap
    ice_cs_conditions.rotor.figure_of_merit = outputs.figure_of_merit
    noise_conditions.rotor                  = outputs  
    power                                   = P
    thrust                                  = F  
    stored_results_flag                     = True
    stored_propulsor_tag                    = ice_cs_propeller.tag
    

    # Compute forces and moments
    moment_vector      = 0*state.ones_row(3)
    F                  = 0*state.ones_row(3)
    F[:,0]             = ice_cs_conditions.thrust[:,0]
    moment_vector[:,0] = ice_cs_propeller.origin[0][0] -   center_of_gravity[0][0] 
    moment_vector[:,1] = ice_cs_propeller.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2] = ice_cs_propeller.origin[0][2]  -  center_of_gravity[0][2]
    M                  =  np.cross(moment_vector, F)   
    moment             = M 
    
    return thrust,moment,power,stored_results_flag,stored_propulsor_tag 
    
def reuse_stored_ice_cs_prop_data(ice_cs_propeller,state,fuel_line,stored_propulsor_tag,center_of_gravity= [[0.0, 0.0,0.0]]):
    '''Reuses results from one ice_cs_propeller for identical propulsors
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure    [-]  
    fuel_line            - fuel_line                              [-] 
    ice_cs_propeller        - ice_cs_propeller data structure     [-] 
    total_thrust         - thrust of ice_cs_propeller group       [N]
    total_power          - power of ice_cs_propeller group        [W] 
     
    Outputs:      
    total_thrust         - thrust of ice_cs_propeller group       [N]
    total_power          - power of ice_cs_propeller group        [W] 
    
    Properties Used: 
    N.A.        
    ''' 
    conditions                                              = state.conditions  
    ice_cs_conditions_0                                     = conditions.energy[fuel_line.tag][stored_propulsor_tag]
    noise_conditions_0                                      = conditions.noise[fuel_line.tag][stored_propulsor_tag] 
    conditions.energy[fuel_line.tag][ice_cs_propeller.tag]  =  ice_cs_conditions_0
    conditions.noise[fuel_line.tag][ice_cs_propeller.tag]   =  noise_conditions_0 

    # compute moment  
    moment_vector      = 0*state.ones_row(3)
    F                  = 0*state.ones_row(3)
    F[:,0]             = ice_cs_conditions_0.thrust[:,0] 
    moment_vector[:,0] = ice_cs_propeller.origin[0][0] -   center_of_gravity[0][0] 
    moment_vector[:,1] = ice_cs_propeller.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2] = ice_cs_propeller.origin[0][2]  -  center_of_gravity[0][2]
    M                  = np.cross(moment_vector, F) 

    moment  = M     
    power   = conditions.energy[fuel_line.tag][ice_cs_propeller.tag].engine.power
    thrust  = conditions.energy[fuel_line.tag][ice_cs_propeller.tag].rotor.thrust 
 
    return thrust,moment,power 
 