## @ingroup Methods-Propulsion
# RCAIDE/Methods/Propulsion/all_electric_propulsor.py
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
# compute_propulsor_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion
def compute_propulsor_performance(i,bus,propulsor_group_tag, ducted_fans,N_ducted_fans,escs,conditions,voltage):
    ''' Computes the perfomrance of an all electric propulsor unit
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs: 
    i                     - index of unique compoment             [-]
    bus_tag               - tag of bus                            [string]
    propulsor_group_tag   - tag of propulsor group                [string]
    motors                - data structure of motors              [-]
    ducted_fans                - data structure of motors              [-]
    N_ducted_fans              - number of ducted_fans in propulsor group   [-]
    escs                  - data structure of motors              [-]
    conditions            - operating data structure              [-]
    voltage               - system voltage                        [Volts]

    Outputs: 
    outputs              - propulsor operating outputs             [-]
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [V]
    total_current        - current of propulsor group             [N]
    
    Properties Used: 
    N.A.        
    '''  
    bus_results               = conditions.energy[bus.tag][propulsor_group_tag]
    noise_pg_results          = conditions.noise[bus.tag][propulsor_group_tag]
    unique_ducted_fan_tags    = bus_results.unique_ducted_fan_tags 
    ducted_fan                = ducted_fans[unique_ducted_fan_tags[i]]
   
    ram                       = ducted_fan.ram
    inlet_nozzle              = ducted_fan.inlet_nozzle
    fan_nozzle                = ducted_fan.fan_nozzle  
    fan                       = ducted_fan.fan
    fan_nozzle                = ducted_fan.fan_nozzle 
    
    #Creating the network by manually linking the different components
    #set the working fluid to determine the fluid properties
    ram.inputs.working_fluid                               = ducted_fan.working_fluid
    
    #Flow through the ram , this computes the necessary flow quantities and stores it into conditions
    ram(conditions)
    
    #link inlet nozzle to ram 
    inlet_nozzle.inputs.stagnation_temperature             = ram.outputs.stagnation_temperature 
    inlet_nozzle.inputs.stagnation_pressure                = ram.outputs.stagnation_pressure 
    
    #Flow through the inlet nozzle
    inlet_nozzle(conditions)
    
    #Link the fan to the inlet nozzle
    fan.inputs.stagnation_temperature                      = inlet_nozzle.outputs.stagnation_temperature
    fan.inputs.stagnation_pressure                         = inlet_nozzle.outputs.stagnation_pressure
    
    #flow through the fan
    fan(conditions)

    #link the fan nozzle to the fan
    fan_nozzle.inputs.stagnation_temperature               = fan.outputs.stagnation_temperature
    fan_nozzle.inputs.stagnation_pressure                  = fan.outputs.stagnation_pressure
    ducted_fan.inputs.fuel_to_air_ratio                        = 0.
    
     # flow through the fan nozzle
    fan_nozzle(conditions)
    
    # compute the thrust using the thrust component
    #link the thrust component to the fan nozzle
    ducted_fan.inputs.fan_exit_velocity                        = fan_nozzle.outputs.velocity
    ducted_fan.inputs.fan_area_ratio                           = fan_nozzle.outputs.area_ratio
    ducted_fan.inputs.fan_nozzle                               = fan_nozzle.outputs
    ducted_fan.inputs.bypass_ratio                             = ducted_fan.bypass_ratio  #0.0
    
    #compute the thrust
    ducted_fan.compute_thrust(conditions, throttle = conditions.energy[bus.tag][propulsor_group_tag].ducted_fan.throttle)

    #obtain the network outputs from the thrust outputs
    u0                    = conditions.freestream.velocity
    u8                    = fan_nozzle.outputs.velocity
   
    eta                   = 2./(1+u8/u0)
    F                     = ducted_fan.outputs.thrust*[1,0,0]
    mdot                  = ducted_fan.outputs.fuel_flow_rate
    Isp                   = ducted_fan.outputs.specific_impulse
    P                     = ducted_fan.outputs.power/eta 
    F_vec                 = conditions.ones_row(3) * 0.0
    F_vec[:,0]            = F[:,0]
    F                     = F_vec 
    
    fan_outputs = Data(
        exit_static_temperature             = fan_nozzle.outputs.static_temperature,
        exit_static_pressure                = fan_nozzle.outputs.static_pressure,
        exit_stagnation_temperature         = fan_nozzle.outputs.stagnation_temperature,
        exit_stagnation_pressure            = fan_nozzle.outputs.static_pressure,
        exit_velocity                       = fan_nozzle.outputs.velocity
        ) 
   
    bus_results.ducted_fan.power             = P
    bus_results.ducted_fan.thrust            = F  
    noise_pg_results.ducted_fan.fan          = fan_outputs
    
    I = P/voltage
    
    return F, P,I, eta,mdot,Isp ,fan_outputs


# ----------------------------------------------------------------------------------------------------------------------
# compute_unique_propulsor_groups
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion
def compute_unique_propulsor_groups(bus): 
    '''Computes the unique ducted_fan groups on a bus    
    
    Assumptions:
    None

    Source:
    N/A

    Inputs: 
    bus                     - bus control unit data structure [-]
    
    Outputs:  
    sorted_propulsors. 
        ducted_fan_indexes       - ducted_fan indexes                   [-]
        unique_ducted_fan_tags   - ducted_fan tags                      [string(s)]
        unique_motor_tags - motor tags                    [string(s)]
        unique_esc_tags   - electronic speed ducted_fan tags     [string(s)]
        N_ducted_fans            - number of ducted_fans                [-]

    Properties Used:
    N/A 
    '''
     
    ducted_fans                = bus.ducted_fans 
    escs                       = bus.electronic_speed_controllers
    active_propulsor_groups    = bus.active_propulsor_groups 
    N_active_propulsor_groups  = len(active_propulsor_groups)
    
    # determine propulsor group indexes  
    ducted_fan_group_indexes,ducted_fan_groups_names,unique_ducted_fan_tags = compute_number_of_compoment_groups(ducted_fans,active_propulsor_groups)
    esc_group_indexes,esc_group_names,unique_esc_tags        = compute_number_of_compoment_groups(escs,active_propulsor_groups)   
    
    # make sure that each ducted_fan has a motor and esc
    if len(ducted_fan_group_indexes)!= len(esc_group_indexes):
        assert('The number of ducted_fans and/or esc is not the same as the number of motors')  
        
    # Count the number of unique pairs of ducted_fans and motors 
    unique_ducted_fan_groups,N_ducted_fans   = np.unique(ducted_fan_group_indexes, return_counts=True) 
    unique_esc_groups,_            = np.unique(esc_group_indexes, return_counts=True)
    if (unique_ducted_fan_groups == unique_esc_groups).all() : # ducted_fans and motors are paired  
        ducted_fan_indexes = [] 
        esc_indexes   = []
        for group in range(N_active_propulsor_groups):
            ducted_fan_indexes.append(np.where(unique_ducted_fan_groups[group] == ducted_fan_group_indexes)[0][0]) 
            esc_indexes.append(np.where(unique_esc_groups[group] == esc_group_indexes)[0][0])  
    else: 
        ducted_fan_indexes = ducted_fan_group_indexes 
        esc_indexes        = esc_group_indexes
        N_ducted_fans      = np.ones_like(ducted_fan_indexes)   
    
    sorted_propulsors = Data(ducted_fan_indexes       = ducted_fan_indexes,
                             unique_ducted_fan_tags   = unique_ducted_fan_tags,  
                             unique_esc_tags     = unique_esc_tags,
                             N_ducted_fans            = N_ducted_fans)
    return sorted_propulsors