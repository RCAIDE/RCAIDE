## @ingroup Methods-Propulsion
# RCAIDE/Methods/Propulsion/internal_combustion_engine_cs_propulsor.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Units , Data  

# pacakge imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# internal_combustion_engine_constant_speed_propulsor
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion
def internal_combustion_engine_cs_propulsor(i,fuel_line_tag,propulsor_group_tag,engines,rotors,N_rotors,conditions): 
    ''' Computes the performance of an internal combustion engine propulsor unit
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs: 
    i                     - index of unique compoment               [-]
    fuel_line_tag          - tag of network                         [string]
    propulsor_group_tag   - tag of propulsor group                  [string]
    engines               - data structure of engines               [-]
    rotors                - data structure of engines               [-]
    N_rotors              - number of rotors in propulsor group     [-]
    escs                  - data structure of engines               [-]
    state                 - operating data structure                [-]
    voltage               - system voltage                          [Volts]
   
    Outputs:    
    outputs              - propulsor operating outputs              [-]
    total_thrust         - thrust of propulsor group                [N]
    total_power          - power of propulsor group                 [V]
    total_current        - current of propulsor group               [N]
    
    Properties Used: 
    N.A.        
    ''' 
    ice_cs_net_pg_results = conditions.energy[fuel_line_tag][propulsor_group_tag]
    noise_pg_results        = conditions.noise[fuel_line_tag][propulsor_group_tag]
    unique_rotor_tags     = ice_cs_net_pg_results.unique_rotor_tags
    unique_engine_tags    = ice_cs_net_pg_results.unique_engine_tags  
    engine                = engines[unique_engine_tags[i]]
    rotor                 = rotors[unique_rotor_tags[i]]  
 
    # Run the rotor to get the power
    rotor.inputs.pitch_command = ice_cs_net_pg_results.rotor.pitch_command
    rotor.inputs.omega         = ice_cs_net_pg_results.engine.rpm
 
    # Spin the rotor 
    F, Q, P, Cp, outputs, etap = rotor.spin(conditions) 

    # Run the engine to calculate the throttle setting and the fuel burn
    engine.inputs.power = P
    engine.calculate_throttle_out_from_power(conditions)

    # Create the outputs 
    R                   = rotor.tip_radius 
    mdot                = engine.outputs.fuel_flow_rate * N_rotors[i]
    rpm                 = engine.inputs.speed / Units.rpm 
    F_mag               = np.atleast_2d(np.linalg.norm(F, axis=1)).T
    throttle            = engine.outputs.throttle  
    total_thrust        = F * N_rotors[i]
    total_power         = P * N_rotors[i]  
      
    # Pack specific outputs
    ice_cs_net_pg_results.mass_flow_rate       = mdot
    ice_cs_net_pg_results.engine.torque        = Q
    ice_cs_net_pg_results.engine.power         = P   
    ice_cs_net_pg_results.engine.throttle      = throttle
    ice_cs_net_pg_results.rotor.torque         = Q
    ice_cs_net_pg_results.rotor.rpm            = rpm
    ice_cs_net_pg_results.rotor.tip_mach       = (R*rpm*Units.rpm)/conditions.freestream.speed_of_sound 
    ice_cs_net_pg_results.rotor.disc_loading   = (F_mag)/(np.pi*(R**2))             
    ice_cs_net_pg_results.rotor.power_loading  = (F_mag)/(P)    
    ice_cs_net_pg_results.rotor.efficiency     = etap
    ice_cs_net_pg_results.rotor.figure_of_merit= outputs.figure_of_merit
    noise_pg_results.rotor                     = outputs 
 
    return outputs , total_thrust , total_power ,mdot
 