## @ingroup Methods-Propulsion
# RCAIDE/Methods/Propulsion/turbojet_propulsor.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Data  
from RCAIDE.Methods.Propulsion.compute_number_of_compoment_groups import compute_number_of_compoment_groups

# pacakge imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# compute_propulsor_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion
def compute_propulsor_performance(i,PCU,propulsor_group_tag,turbojets,N_turbojets,conditions): 
    ''' 
    ''' 
    unique_turbojet_tags  = conditions.energy[PCU.tag][propulsor_group_tag].unique_turbojet_tags 
    turbojet              = turbojets[unique_turbojet_tags[i]] 

    ram                       = turbojet.ram
    inlet_nozzle              = turbojet.inlet_nozzle
    low_pressure_compressor   = turbojet.low_pressure_compressor
    high_pressure_compressor  = turbojet.high_pressure_compressor
    combustor                 = turbojet.combustor
    high_pressure_turbine     = turbojet.high_pressure_turbine
    low_pressure_turbine      = turbojet.low_pressure_turbine
    try:
        afterburner           = turbojet.afterburner
    except:
        pass
    core_nozzle               = turbojet.core_nozzle  

    #Creating the network by manually linking the different components

    #set the working fluid to determine the fluid properties
    ram.inputs.working_fluid                               = turbojet.working_fluid

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

    #link the combustor to the high pressure compressor
    combustor.inputs.stagnation_temperature                = high_pressure_compressor.outputs.stagnation_temperature
    combustor.inputs.stagnation_pressure                   = high_pressure_compressor.outputs.stagnation_pressure

    #flow through the high pressor comprresor
    combustor(conditions)

    #link the high pressure turbine to the combustor
    high_pressure_turbine.inputs.stagnation_temperature    = combustor.outputs.stagnation_temperature
    high_pressure_turbine.inputs.stagnation_pressure       = combustor.outputs.stagnation_pressure
    high_pressure_turbine.inputs.fuel_to_air_ratio         = combustor.outputs.fuel_to_air_ratio

    #link the high pressuer turbine to the high pressure compressor
    high_pressure_turbine.inputs.compressor                = high_pressure_compressor.outputs

    #flow through the high pressure turbine
    high_pressure_turbine(conditions)

    #link the low pressure turbine to the high pressure turbine
    low_pressure_turbine.inputs.stagnation_temperature     = high_pressure_turbine.outputs.stagnation_temperature
    low_pressure_turbine.inputs.stagnation_pressure        = high_pressure_turbine.outputs.stagnation_pressure

    #link the low pressure turbine to the low_pressure_compresor
    low_pressure_turbine.inputs.compressor                 = low_pressure_compressor.outputs

    #link the low pressure turbine to the combustor
    low_pressure_turbine.inputs.fuel_to_air_ratio          = combustor.outputs.fuel_to_air_ratio

    #get the bypass ratio from the thrust component
    low_pressure_turbine.inputs.bypass_ratio               = 0.0

    #flow through the low pressure turbine
    low_pressure_turbine(conditions)

    if turbojet.afterburner_active == True:
        #link the core nozzle to the afterburner
        afterburner.inputs.stagnation_temperature              = low_pressure_turbine.outputs.stagnation_temperature
        afterburner.inputs.stagnation_pressure                 = low_pressure_turbine.outputs.stagnation_pressure   
        afterburner.inputs.nondim_ratio                        = 1.0 + combustor.outputs.fuel_to_air_ratio

        #flow through the afterburner
        afterburner(conditions)

        #link the core nozzle to the afterburner
        core_nozzle.inputs.stagnation_temperature              = afterburner.outputs.stagnation_temperature
        core_nozzle.inputs.stagnation_pressure                 = afterburner.outputs.stagnation_pressure   

    else:
        #link the core nozzle to the low pressure turbine
        core_nozzle.inputs.stagnation_temperature              = low_pressure_turbine.outputs.stagnation_temperature
        core_nozzle.inputs.stagnation_pressure                 = low_pressure_turbine.outputs.stagnation_pressure

    #flow through the core nozzle
    core_nozzle(conditions)

    # compute the thrust using the thrust component
    #link the thrust component to the core nozzle
    turbojet.inputs.core_exit_velocity                       = core_nozzle.outputs.velocity
    turbojet.inputs.core_area_ratio                          = core_nozzle.outputs.area_ratio
    turbojet.inputs.core_nozzle                              = core_nozzle.outputs

    #link the thrust component to the combustor
    turbojet.inputs.fuel_to_air_ratio                        = combustor.outputs.fuel_to_air_ratio 
    if turbojet.afterburner_active == True:
        # previous fuel ratio is neglected when the afterburner fuel ratio is calculated
        turbojet.inputs.fuel_to_air_ratio += afterburner.outputs.fuel_to_air_ratio

    #link the thrust component to the low pressure compressor 
    turbojet.inputs.total_temperature_reference              = low_pressure_compressor.outputs.stagnation_temperature
    turbojet.inputs.total_pressure_reference                 = low_pressure_compressor.outputs.stagnation_pressure 
    turbojet.inputs.flow_through_core                        =  1.0 #scaled constant to turn on core thrust computation
    turbojet.inputs.flow_through_fan                         =  0.0 #scaled constant to turn on fan thrust computation        

    #compute the thrust
    turbojet.compute_thrust(conditions,throttle = conditions.energy[PCU.tag][propulsor_group_tag].turbofan.throttle )

    #getting the network outputs from the thrust outputs
    F            = turbojet.outputs.thrust*[1,0,0]
    mdot         = turbojet.outputs.fuel_flow_rate
    Isp          = turbojet.outputs.specific_impulse
    P            = turbojet.outputs.power
    F_vec        = conditions.ones_row(3) * 0.0
    F_vec[:,0]   = F[:,0]
    F            = F_vec

    results = Data()
    results.thrust_force_vector         = F
    results.vehicle_mass_rate           = mdot  
    
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
     
    turbojets                  = PCU.turbojets
    active_propulsor_groups    = PCU.active_propulsor_groups
    
    # determine propulsor group indexes 
    turbojet_group_indexes,turbojet_group_names,unique_turbojet_tags = compute_number_of_compoment_groups(turbojets,active_propulsor_groups)   

    # Count the number of unique pairs of rotors and engines 
    unique_turbojet_groups,N_turbojets     = np.unique(turbojet_group_indexes, return_counts=True)   
    
    sorted_propulsors = Data(unique_turbojet_tags  = unique_turbojet_tags, 
                             N_turbojets           = N_turbojets[0])
    return sorted_propulsors