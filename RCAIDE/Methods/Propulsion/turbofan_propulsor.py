## @ingroup Methods-Propulsion
# RCAIDE/Methods/Propulsion/turbofan_propulsor.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Data 
from RCAIDE.Analyses.Mission.Common.Conditions import Conditions
from RCAIDE.Methods.Propulsion.compute_number_of_compoment_groups import compute_number_of_compoment_groups

# pacakge imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# compute_propulsor_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion
def compute_propulsor_performance(i,PCU,propulsor_group_tag,turbofans,N_turbofans,conditions): 
    ''' 
    ''' 
    unique_turbofan_tags  = conditions.energy[PCU.tag][propulsor_group_tag].unique_turbofan_tags 
    turbofan              = turbofans[unique_turbofan_tags[i]]
   
    ram                       = turbofan.ram
    inlet_nozzle              = turbofan.inlet_nozzle
    low_pressure_compressor   = turbofan.low_pressure_compressor
    high_pressure_compressor  = turbofan.high_pressure_compressor
    fan                       = turbofan.fan
    combustor                 = turbofan.combustor
    high_pressure_turbine     = turbofan.high_pressure_turbine
    low_pressure_turbine      = turbofan.low_pressure_turbine
    core_nozzle               = turbofan.core_nozzle
    fan_nozzle                = turbofan.fan_nozzle 
    bypass_ratio              = turbofan.bypass_ratio 

    #Creating the network by manually linking the different components

    #set the working fluid to determine the fluid properties
    ram.inputs.working_fluid                               = turbofan.working_fluid

    #Flow through the ram , this computes the necessary flow quantities and stores it into conditions
    ram(conditions) 

    #link inlet nozzle to ram 
    inlet_nozzle.inputs.stagnation_temperature             = ram.outputs.stagnation_temperature 
    inlet_nozzle.inputs.stagnation_pressure                = ram.outputs.stagnation_pressure

    #Flow through the inlet nozzle
    inlet_nozzle(conditions)

    #--link low pressure compressor to the inlet nozzle
    low_pressure_compressor.inputs.stagnation_temperature  = inlet_nozzle.outputs.stagnation_temperature
    low_pressure_compressor.inputs.stagnation_pressure     = inlet_nozzle.outputs.stagnation_pressure

    #Flow through the low pressure compressor
    low_pressure_compressor(conditions)

    #link the high pressure compressor to the low pressure compressor
    high_pressure_compressor.inputs.stagnation_temperature = low_pressure_compressor.outputs.stagnation_temperature
    high_pressure_compressor.inputs.stagnation_pressure    = low_pressure_compressor.outputs.stagnation_pressure

    #Flow through the high pressure compressor
    high_pressure_compressor(conditions)

    #Link the fan to the inlet nozzle
    fan.inputs.stagnation_temperature                      = inlet_nozzle.outputs.stagnation_temperature
    fan.inputs.stagnation_pressure                         = inlet_nozzle.outputs.stagnation_pressure

    #flow through the fan
    fan(conditions)

    #link the combustor to the high pressure compressor
    combustor.inputs.stagnation_temperature                = high_pressure_compressor.outputs.stagnation_temperature
    combustor.inputs.stagnation_pressure                   = high_pressure_compressor.outputs.stagnation_pressure

    #flow through the high pressor comprresor
    combustor(conditions)

    # link the shaft power output to the low pressure compressor
    try:
        shaft_power = turbofan.Shaft_Power_Off_Take       
        shaft_power.inputs.mdhc                            = turbofan.compressor_nondimensional_massflow
        shaft_power.inputs.Tref                            = turbofan.reference_temperature
        shaft_power.inputs.Pref                            = turbofan.reference_pressure
        shaft_power.inputs.total_temperature_reference     = low_pressure_compressor.outputs.stagnation_temperature
        shaft_power.inputs.total_pressure_reference        = low_pressure_compressor.outputs.stagnation_pressure

        shaft_power(conditions)
    except:
        pass

    #link the high pressure turbine to the combustor
    high_pressure_turbine.inputs.stagnation_temperature    = combustor.outputs.stagnation_temperature
    high_pressure_turbine.inputs.stagnation_pressure       = combustor.outputs.stagnation_pressure
    high_pressure_turbine.inputs.fuel_to_air_ratio         = combustor.outputs.fuel_to_air_ratio

    #link the high pressuer turbine to the high pressure compressor
    high_pressure_turbine.inputs.compressor                = high_pressure_compressor.outputs

    #link the high pressure turbine to the fan
    high_pressure_turbine.inputs.fan                       = fan.outputs
    high_pressure_turbine.inputs.bypass_ratio              = 0.0 #set to zero to ensure that fan not linked here

    #flow through the high pressure turbine
    high_pressure_turbine(conditions)

    #link the low pressure turbine to the high pressure turbine
    low_pressure_turbine.inputs.stagnation_temperature     = high_pressure_turbine.outputs.stagnation_temperature
    low_pressure_turbine.inputs.stagnation_pressure        = high_pressure_turbine.outputs.stagnation_pressure

    #link the low pressure turbine to the low_pressure_compresor
    low_pressure_turbine.inputs.compressor                 = low_pressure_compressor.outputs

    #link the low pressure turbine to the combustor
    low_pressure_turbine.inputs.fuel_to_air_ratio          = combustor.outputs.fuel_to_air_ratio

    #link the low pressure turbine to the fan
    low_pressure_turbine.inputs.fan                        = fan.outputs

    # link the low pressure turbine to the shaft power, if needed
    try:
        low_pressure_turbine.inputs.shaft_power_off_take   = shaft_power.outputs
    except:
        pass

    #get the bypass ratio from the thrust component
    low_pressure_turbine.inputs.bypass_ratio               = bypass_ratio

    #flow through the low pressure turbine
    low_pressure_turbine(conditions)

    #link the core nozzle to the low pressure turbine
    core_nozzle.inputs.stagnation_temperature              = low_pressure_turbine.outputs.stagnation_temperature
    core_nozzle.inputs.stagnation_pressure                 = low_pressure_turbine.outputs.stagnation_pressure

    #flow through the core nozzle
    core_nozzle(conditions)

    #link the dan nozzle to the fan
    fan_nozzle.inputs.stagnation_temperature               = fan.outputs.stagnation_temperature
    fan_nozzle.inputs.stagnation_pressure                  = fan.outputs.stagnation_pressure

    # flow through the fan nozzle
    fan_nozzle(conditions)

    # compute the thrust using the thrust component
    #link the thrust component to the fan nozzle
    turbofan.inputs.fan_exit_velocity                        = fan_nozzle.outputs.velocity
    turbofan.inputs.fan_area_ratio                           = fan_nozzle.outputs.area_ratio
    turbofan.inputs.fan_nozzle                               = fan_nozzle.outputs

    #link the thrust component to the core nozzle
    turbofan.inputs.core_exit_velocity                       = core_nozzle.outputs.velocity
    turbofan.inputs.core_area_ratio                          = core_nozzle.outputs.area_ratio
    turbofan.inputs.core_nozzle                              = core_nozzle.outputs

    #link the thrust component to the combustor
    turbofan.inputs.fuel_to_air_ratio                        = combustor.outputs.fuel_to_air_ratio

    #link the thrust component to the low pressure compressor 
    turbofan.inputs.total_temperature_reference              = low_pressure_compressor.outputs.stagnation_temperature
    turbofan.inputs.total_pressure_reference                 = low_pressure_compressor.outputs.stagnation_pressure 
    turbofan.inputs.bypass_ratio                             = bypass_ratio
    turbofan.inputs.flow_through_core                        = 1./(1.+bypass_ratio) #scaled constant to turn on core thrust computation
    turbofan.inputs.flow_through_fan                         = bypass_ratio/(1.+bypass_ratio) #scaled constant to turn on fan thrust computation        

    #compute the thrust
    turbofan.compute_thrust(conditions,throttle = conditions.energy[PCU.tag][propulsor_group_tag].turbofan.throttle )

    #getting the network outputs from the thrust outputs
    F            = turbofan.outputs.thrust*[1,0,0]*N_turbofans
    mdot         = turbofan.outputs.fuel_flow_rate*N_turbofans
    P            = turbofan.outputs.power*N_turbofans
    F_vec        = conditions.ones_row(3) * 0.0
    F_vec[:,0]   = F[:,0] 
    
    # store data
    core_outputs = Data(
        exit_static_temperature             = core_nozzle.outputs.static_temperature,
        exit_static_pressure                = core_nozzle.outputs.static_pressure,
        exit_stagnation_temperature         = core_nozzle.outputs.stagnation_temperature,
        exit_stagnation_pressure            = core_nozzle.outputs.static_pressure,
        exit_velocity                       = core_nozzle.outputs.velocity
        )
    
    fan_outputs = Data(
        exit_static_temperature             = fan_nozzle.outputs.static_temperature,
        exit_static_pressure                = fan_nozzle.outputs.static_pressure,
        exit_stagnation_temperature         = fan_nozzle.outputs.stagnation_temperature,
        exit_stagnation_pressure            = fan_nozzle.outputs.static_pressure,
        exit_velocity                       = fan_nozzle.outputs.velocity
        )
    
    conditions.noise.sources.turbofan       = Conditions()        
    conditions.noise.sources.turbofan.fan   = fan_outputs
    conditions.noise.sources.turbofan.core  = core_outputs
    
    return F_vec, P , mdot


# ----------------------------------------------------------------------------------------------------------------------
# compute_unique_propulsor_groups
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion
def compute_unique_propulsor_groups(PCU): 
    '''Computes the unique rotor groups on a PCU    
    
    Assumptions:
    None

    Source:
    N/A

    Inputs: 
    PCU                     - power control unit control unit data structure [-]
    
    Outputs:  
    sorted_propulsors. 
        rotor_indexes       - rotor indexes                   [-]
        unique_rotor_tags   - rotor tags                      [string(s)]
        unique_motor_tags   - motor tags                      [string(s)]
        unique_esc_tags     - electronic speed rotor tags     [string(s)]
        N_rotors            - number of rotors                [-]

    Properties Used:
    N/A 
    '''
     
    turbofans                  = PCU.turbofans
    active_propulsor_groups    = PCU.active_propulsor_groups
    
    # determine propulsor group indexes 
    turbofan_group_indexes,turbofan_group_names,unique_turbofan_tags = compute_number_of_compoment_groups(turbofans,active_propulsor_groups)   

    # Count the number of unique pairs of rotors and engines 
    unique_turbofan_groups,N_turbofans     = np.unique(turbofan_group_indexes, return_counts=True)   
    
    sorted_propulsors = Data(unique_turbofan_tags  = unique_turbofan_tags, 
                             N_turbofans           = N_turbofans[0])
    return sorted_propulsors