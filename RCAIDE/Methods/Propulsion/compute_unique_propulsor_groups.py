# RCAIDE/Methods/Propulsion/compute_unique_propulsor_groups.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
from RCAIDE.Core import Data

# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion
def compute_unique_propulsor_groups(bus):   
    
    motors                     = bus.motors 
    rotors                     = bus.rotors 
    escs                       = bus.electronic_speed_controllers
    active_propulsor_groups    = bus.active_propulsor_groups 
    N_active_propulsor_groups = len(active_propulsor_groups)
    
    # determine propulsor group indexes 
    motor_group_indexes,motor_group_names,unique_motor_tags  = compute_number_of_compoment_groups(motors,active_propulsor_groups)
    rotor_group_indexes,rotor_groups_names,unique_rotor_tags = compute_number_of_compoment_groups(rotors,active_propulsor_groups)
    esc_group_indexes,esc_group_names,unique_esc_tags        = compute_number_of_compoment_groups(escs,active_propulsor_groups)   
    
    # make sure that each rotor has a motor and esc
    if (len(rotor_group_indexes)!=len(motor_group_indexes)) or (len(esc_group_indexes)!=len(motor_group_indexes)):
        assert('The number of rotors and/or esc is not the same as the number of motors')  
        
    # Count the number of unique pairs of rotors and motors 
    unique_rotor_groups,N_rotors   = np.unique(rotor_group_indexes, return_counts=True)
    unique_motor_groups,_          = np.unique(motor_group_indexes, return_counts=True)
    unique_esc_groups,_            = np.unique(esc_group_indexes, return_counts=True)
    if (unique_rotor_groups == unique_motor_groups).all() and (unique_esc_groups == unique_motor_groups).all(): # rotors and motors are paired  
        rotor_indexes = []
        motor_indexes = []
        esc_indexes   = []
        for group in range(N_active_propulsor_groups):
            rotor_indexes.append(np.where(unique_rotor_groups[group] == rotor_group_indexes)[0][0])
            motor_indexes.append(np.where(unique_motor_groups[group] == motor_group_indexes)[0][0])
            esc_indexes.append(np.where(unique_esc_groups[group] == esc_group_indexes)[0][0])  
    else: 
        rotor_indexes = rotor_group_indexes
        motor_indexes = motor_group_indexes
        esc_indexes   = esc_group_indexes
        N_rotors      = np.ones_like(motor_group_indexes)   
    
    Res = Data(
               rotor_indexes       = rotor_indexes,
               unique_rotor_tags   = unique_rotor_tags,
               unique_motor_tags   = unique_motor_tags,
               unique_esc_tags     = unique_esc_tags,
               N_rotors            = N_rotors)
    return Res


def compute_number_of_compoment_groups(components,active_propulsor_groups): 
    ''''
    
    # loop through motors and determine the number of propulsor groups
    
    ''' 
    comp_groups        = [] 
    comp_group_indexes = []
    group_iterator     = 0 
    unique_tags        = []
    for comp in components: 
        for i in range(len(active_propulsor_groups)):  
            if comp.propulsor_group == active_propulsor_groups[i]:
                if (comp.propulsor_group) in comp_groups: 
                    # find index in list  
                    c_i = comp_groups.index(comp.propulsor_group)
                    
                    # append it to group index 
                    comp_group_indexes.append(c_i)
                    
                else: 
                    unique_tags.append(comp.tag)
                    comp_groups.append(comp.propulsor_group)
        
                    # append it to group index 
                    comp_group_indexes.append(group_iterator) 
                    
                    # increment iterator 
                    group_iterator+= 1  
    return comp_group_indexes,comp_groups,unique_tags  