## @ingroup Methods-Propulsion
# RCAIDE/Methods/Propulsion/internal_combustion_engine_constant_speed_propulsor.py
# 
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
def compute_propulsor_performance(i,fuel_line_tag,propulsor_group_tag,engines,rotors,N_rotors,conditions): 
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
    unique_rotor_tags   = conditions.energy[fuel_line_tag][propulsor_group_tag].unique_rotor_tags
    unique_engine_tags  = conditions.energy[fuel_line_tag][propulsor_group_tag].unique_engine_tags  
    engine              = engines[unique_engine_tags[i]]
    rotor               = rotors[unique_rotor_tags[i]]  
 
    # Run the rotor to get the power
    rotor.inputs.pitch_command = conditions.energy[fuel_line_tag][propulsor_group_tag].rotor.pitch_command
    rotor.inputs.omega         = conditions.energy[fuel_line_tag][propulsor_group_tag].engine.rpm
 
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
    conditions.energy[fuel_line_tag][propulsor_group_tag].mass_flow_rate       = mdot
    conditions.energy[fuel_line_tag][propulsor_group_tag].engine.torque        = Q
    conditions.energy[fuel_line_tag][propulsor_group_tag].engine.power         = P   
    conditions.energy[fuel_line_tag][propulsor_group_tag].engine.throttle      = throttle
    conditions.energy[fuel_line_tag][propulsor_group_tag].rotor.torque         = Q
    conditions.energy[fuel_line_tag][propulsor_group_tag].rotor.rpm            = rpm
    conditions.energy[fuel_line_tag][propulsor_group_tag].rotor.tip_mach       = (R*rpm*Units.rpm)/conditions.freestream.speed_of_sound 
    conditions.energy[fuel_line_tag][propulsor_group_tag].rotor.disc_loading   = (F_mag)/(np.pi*(R**2))             
    conditions.energy[fuel_line_tag][propulsor_group_tag].rotor.power_loading  = (F_mag)/(P)    
    conditions.energy[fuel_line_tag][propulsor_group_tag].rotor.efficiency     = etap
    conditions.energy[fuel_line_tag][propulsor_group_tag].rotor.figure_of_merit= outputs.figure_of_merit
    conditions.noise.sources.rotors[rotor.tag]                                 = outputs 
 
    return outputs , total_thrust , total_power ,mdot

def compute_unique_propulsor_groups(self): 
    '''Computes the unique rotor groups on a bus    
    
    Assumptions:
    None

    Source:
    N/A

    Inputs: 
    bus                     - bus control unit data structure [-]
    
    Outputs:  
    sorted_propulsors. 
        rotor_indexes       - rotor indexes                   [-]
        unique_rotor_tags   - rotor tags                      [string(s)]
        unique_engine_tags  - engine tags                     [string(s)]
        unique_esc_tags     - electronic speed rotor tags     [string(s)]
        N_rotors            - number of rotors                [-]

    Properties Used:
    N/A 
    '''
    
    engines                    = self.engines 
    rotors                     = self.rotors  
    active_propulsor_groups    = self.active_propulsor_groups 
    N_active_propulsor_groups  = len(active_propulsor_groups)
    
    # determine propulsor group indexes 
    engine_group_indexes,engine_group_names,unique_engine_tags  = compute_number_of_compoment_groups(engines,active_propulsor_groups)
    rotor_group_indexes,rotor_groups_names,unique_rotor_tags    = compute_number_of_compoment_groups(rotors,active_propulsor_groups) 
    
    # make sure that each rotor has a engine and esc
    if (len(rotor_group_indexes)!=len(engine_group_indexes)):
        assert('The number of rotors and/or esc is not the same as the number of engines')  
        
    # Count the number of unique pairs of rotors and engines 
    unique_rotor_groups,N_rotors   = np.unique(rotor_group_indexes, return_counts=True)
    unique_engine_groups,_                 = np.unique(engine_group_indexes, return_counts=True) 
    if (unique_rotor_groups == unique_engine_groups).all(): 
        rotor_indexes  = []
        engine_indexes = [] 
        for group in range(N_active_propulsor_groups):
            rotor_indexes.append(np.where(unique_rotor_groups[group]   == rotor_group_indexes)[0][0])
            engine_indexes.append(np.where(unique_engine_groups[group] == engine_group_indexes)[0][0]) 
    else: 
        rotor_indexes = rotor_group_indexes
        engine_indexes = engine_group_indexes 
        N_rotors      = np.ones_like(engine_group_indexes)   
    
    sorted_propulsors = Data(rotor_indexes       = rotor_indexes,
                             unique_rotor_tags   = unique_rotor_tags,
                             unique_engine_tags      = unique_engine_tags, 
                             N_rotors            = N_rotors)
    return sorted_propulsors
