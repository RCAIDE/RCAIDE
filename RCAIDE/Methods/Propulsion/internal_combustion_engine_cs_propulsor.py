# RCAIDE/Methods/Propulsion/internal_combustion_engine_constant_speed_propulsor.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Units , Data 
from RCAIDE.Methods.Propulsion.compute_number_of_compoment_groups import compute_number_of_compoment_groups

# pacakge imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# compute_ICE_propulsor_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion
def compute_propulsor_performance(i,network_tag,propulsor_group_tag,engines,propellers,N_propellers,state,): 
    ''' Computes the performance of an internal combustion engine propulsor unit
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs: 
    i                     - index of unique compoment               [-]
    network_tag           - tag of network                          [string]
    propulsor_group_tag   - tag of propulsor group                  [string]
    engines               - data structure of engines               [-]
    propellers            - data structure of engines               [-]
    N_propellers          - number of propellers in propulsor group [-]
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
    unique_propeller_tags   = state.conditions.energy[network_tag][propulsor_group_tag].unique_propeller_tags
    unique_engine_tags      = state.conditions.energy[network_tag][propulsor_group_tag].unique_engine_tags  
    engine                  = engines[unique_engine_tags[i]]
    propeller               = propellers[unique_propeller_tags[i]]  
 
    # Run the propeller to get the power
    propeller.inputs.pitch_command = state.conditions.energy.throttle - 0.5
    propeller.inputs.omega         = state.conditions.energy.rpm
 
    # Spin the propeller 
    F, Q, P, Cp, outputs, etap = propeller.spin(state.conditions) 

    # Run the engine to calculate the throttle setting and the fuel burn
    engine.inputs.power = P
    engine.calculate_throttle(state.conditions)

    # Create the outputs 
    R                   = propeller.tip_radius 
    mdot                = mdot + engine.outputs.fuel_flow_rate * N_propellers[i]
    rpm                 = engine.inputs.speed / Units.rpm 
    F_mag               = np.atleast_2d(np.linalg.norm(F, axis=1)).T
    throttle            = engine.outputs.throttle  
    total_thrust        = F * N_propellers[i]
    total_power         = P * N_propellers[i]  
      
    # Pack specific outputs
    state.conditions.energy[network_tag][propulsor_group_tag].engine_torque            = Q
    state.conditions.energy[network_tag][propulsor_group_tag].propeller.torque         = Q
    state.conditions.energy[network_tag][propulsor_group_tag].propeller.rpm            = rpm
    state.conditions.energy[network_tag][propulsor_group_tag].propeller.tip_mach       = (R*rpm*Units.rpm)/a
    state.conditions.energy[network_tag][propulsor_group_tag].propeller.disc_loading   = (F_mag)/(np.pi*(R**2))             
    state.conditions.energy[network_tag][propulsor_group_tag].propeller.power_loading  = (F_mag)/(P)    
    state.conditions.energy[network_tag][propulsor_group_tag].propeller.efficiency     = etap
    state.conditions.energy[network_tag][propulsor_group_tag].propeller.figure_of_merit= outputs.figure_of_merit
    state.conditions.energy[network_tag][propulsor_group_tag].throttle                 = throttle
    state.conditions.noise.sources.propellers[propeller.tag]                           = outputs 
 
    return outputs , total_thrust , total_power 

def compute_unique_propulsor_groups(self): 
    '''Computes the unique propeller groups on a bus    
    
    Assumptions:
    None

    Source:
    N/A

    Inputs: 
    bus                     - bus control unit data structure [-]
    
    Outputs:  
    sorted_propulsors. 
        propeller_indexes       - propeller indexes                   [-]
        unique_propeller_tags   - propeller tags                      [string(s)]
        unique_engine_tags  - engine tags                     [string(s)]
        unique_esc_tags     - electronic speed propeller tags     [string(s)]
        N_propellers            - number of propellers                [-]

    Properties Used:
    N/A 
    '''
    
    engines                    = self.engines 
    propellers                 = self.propellers  
    active_propulsor_groups    = self.active_propulsor_groups 
    N_active_propulsor_groups  = len(active_propulsor_groups)
    
    # determine propulsor group indexes 
    engine_group_indexes,engine_group_names,unique_engine_tags  = compute_number_of_compoment_groups(engines,active_propulsor_groups)
    propeller_group_indexes,propeller_groups_names,unique_propeller_tags    = compute_number_of_compoment_groups(propellers,active_propulsor_groups) 
    
    # make sure that each propeller has a engine and esc
    if (len(propeller_group_indexes)!=len(engine_group_indexes)):
        assert('The number of propellers and/or esc is not the same as the number of engines')  
        
    # Count the number of unique pairs of propellers and engines 
    unique_propeller_groups,N_propellers   = np.unique(propeller_group_indexes, return_counts=True)
    unique_engine_groups,_                 = np.unique(engine_group_indexes, return_counts=True) 
    if (unique_propeller_groups == unique_engine_groups).all(): 
        propeller_indexes  = []
        engine_indexes = [] 
        for group in range(N_active_propulsor_groups):
            propeller_indexes.append(np.where(unique_propeller_groups[group]   == propeller_group_indexes)[0][0])
            engine_indexes.append(np.where(unique_engine_groups[group] == engine_group_indexes)[0][0]) 
    else: 
        propeller_indexes = propeller_group_indexes
        engine_indexes = engine_group_indexes 
        N_propellers      = np.ones_like(engine_group_indexes)   
    
    sorted_propulsors = Data(propeller_indexes       = propeller_indexes,
                             unique_propeller_tags   = unique_propeller_tags,
                             unique_engine_tags      = unique_engine_tags, 
                             N_propellers            = N_propellers)
    return sorted_propulsors
