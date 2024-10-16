## @ingroup Methods-Energy-Propulsors-Turbofan_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Turbofan_Propulsor/compute_turbofan_performance.py
# 
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Framework.Core import Data   
from RCAIDE.Library.Methods.Propulsors.Converters.Ram                import compute_ram_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Combustor          import compute_combustor_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Compressor         import compute_compressor_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Fan                import compute_fan_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Turbine            import compute_turbine_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Expansion_Nozzle   import compute_expansion_nozzle_performance 
from RCAIDE.Library.Methods.Propulsors.Converters.Compression_Nozzle import compute_compression_nozzle_performance
from RCAIDE.Library.Methods.Propulsors.Turbofan_Propulsor            import compute_thrust

import  numpy as  np

# ----------------------------------------------------------------------------------------------------------------------
# compute_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsors-Turbofan_Propulsor
def compute_turbofan_performance(fuel_line,state,center_of_gravity=[[0.0, 0.0, 0.0]]):  
    ''' Computes the perfomrance of all turbofan engines connected to a fuel tank
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:   
    fuel_line            - data structure containing turbofans on distrubution network  [-]  
    propulsors           - list of propulsors that are powered by energy source         [-]
    state                - operating data structure                                     [-] 
                     
    Outputs:                      
    outputs              - turbofan operating outputs                                   [-]
    total_thrust         - thrust of turbofans                                          [N]
    total_power          - power of turbofans                                           [W] 
    
    Properties Used: 
    N.A.        
    '''
   
    total_power     = 0*state.ones_row(1) 
    total_thrust    = 0*state.ones_row(3)
    total_moment    = 0*state.ones_row(3)
    stored_results_flag  = False  
    
    for turbofan in fuel_line.propulsors:  
        if turbofan.active == True:  
            if fuel_line.identical_propulsors == False:
                # run analysis  
                total_thrust,total_moment,total_power ,stored_results_flag,stored_propulsor_tag = compute_performance(state,fuel_line,turbofan,total_thrust,total_moment,total_power,center_of_gravity)
            else:             
                if stored_results_flag == False: 
                    # run analysis 
                    total_thrust,total_moment,total_power ,stored_results_flag,stored_propulsor_tag = compute_performance(state,fuel_line,turbofan,total_thrust,total_moment,total_power,center_of_gravity)
                else:
                    # use old results 
                    total_thrust,total_moment,total_power  = reuse_stored_data(state,fuel_line,turbofan,stored_propulsor_tag,total_thrust,total_moment,total_power,center_of_gravity)
                
    return total_thrust,total_moment,total_power

def compute_performance(state,fuel_line,turbofan,total_thrust,total_moment,total_power, center_of_gravity= [[0.0, 0.0,0.0]]):  
    ''' Computes the perfomrance of one turbofan
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure   [-]  
    fuel_line            - fuelline                              [-] 
    turbofan             - turbofan data structure               [-] 
    total_thrust         - thrust of turbofan group              [N]
    total_power          - power of turbofan group               [W] 

    Outputs:  
    total_thrust         - thrust of turbofan group              [N]
    total_power          - power of turbofan group               [W] 
    stored_results_flag  - boolean for stored results            [-]     
    stored_propulsor_tag - name of turbofan with stored results  [-]
    
    Properties Used: 
    N.A.        
    ''' 
    conditions                = state.conditions   
    noise_conditions          = conditions.noise[fuel_line.tag][turbofan.tag] 
    turbofan_conditions       = conditions.energy[fuel_line.tag][turbofan.tag] 
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
    
    # unpack component conditions 
    ram_conditions          = turbofan_conditions[ram.tag]    
    fan_conditions          = turbofan_conditions[fan.tag]    
    inlet_nozzle_conditions = turbofan_conditions[inlet_nozzle.tag]
    core_nozzle_conditions  = turbofan_conditions[core_nozzle.tag]
    fan_nozzle_conditions   = turbofan_conditions[fan_nozzle.tag]
    lpc_conditions          = turbofan_conditions[low_pressure_compressor.tag]
    hpc_conditions          = turbofan_conditions[high_pressure_compressor.tag]
    lpt_conditions          = turbofan_conditions[low_pressure_turbine.tag]
    hpt_conditions          = turbofan_conditions[high_pressure_turbine.tag]
    combustor_conditions    = turbofan_conditions[combustor.tag]
    freestream              = conditions.freestream

    #Creating the network by manually linking the different components

    #set the working fluid to determine the fluid properties
    ram.working_fluid                               = turbofan.working_fluid

    #Flow through the ram , this computes the necessary flow quantities and stores it into conditions
    compute_ram_performance(ram,ram_conditions, freestream)

    #link inlet nozzle to ram 
    inlet_nozzle_conditions.inputs.stagnation_temperature             = ram_conditions.outputs.stagnation_temperature 
    inlet_nozzle_conditions.inputs.stagnation_pressure                = ram_conditions.outputs.stagnation_pressure

    #Flow through the inlet nozzle
    compute_compression_nozzle_performance(inlet_nozzle,inlet_nozzle_conditions, freestream)

    #--link low pressure compressor to the inlet nozzle
    lpc_conditions.inputs.stagnation_temperature  = inlet_nozzle_conditions.outputs.stagnation_temperature
    lpc_conditions.inputs.stagnation_pressure     = inlet_nozzle_conditions.outputs.stagnation_pressure

    #Flow through the low pressure compressor
    compute_compressor_performance(low_pressure_compressor,lpc_conditions, freestream)

    #link the high pressure compressor to the low pressure compressor
    hpc_conditions.inputs.stagnation_temperature = lpc_conditions.outputs.stagnation_temperature
    hpc_conditions.inputs.stagnation_pressure    = lpc_conditions.outputs.stagnation_pressure

    #Flow through the high pressure compressor
    compute_compressor_performance(high_pressure_compressor,hpc_conditions, freestream)

    #Link the fan to the inlet nozzle
    fan_conditions.inputs.stagnation_temperature                      = inlet_nozzle_conditions.outputs.stagnation_temperature
    fan_conditions.inputs.stagnation_pressure                         = inlet_nozzle_conditions.outputs.stagnation_pressure

    #flow through the fan
    compute_fan_performance(fan,fan_conditions, freestream)

    #link the combustor to the high pressure compressor
    combustor_conditions.inputs.stagnation_temperature                = hpc_conditions.outputs.stagnation_temperature
    combustor_conditions.inputs.stagnation_pressure                   = hpc_conditions.outputs.stagnation_pressure

    #flow through the high pressor comprresor
    compute_combustor_performance(combustor,combustor_conditions, freestream)

    # link the shaft power output to the low pressure compressor
    try:
        shaft_power = turbofan.Shaft_Power_Off_Take       
        shaft_power.inputs.mdhc                            = turbofan.compressor_nondimensional_massflow
        shaft_power.inputs.Tref                            = turbofan.reference_temperature
        shaft_power.inputs.Pref                            = turbofan.reference_pressure
        shaft_power.inputs.total_temperature_reference     = lpc_conditions.outputs.stagnation_temperature
        shaft_power.inputs.total_pressure_reference        = lpc_conditions.outputs.stagnation_pressure

        shaft_power(conditions)
        lpt_conditions.inputs.shaft_power_off_take   = shaft_power.outputs
    except:
        lpt_conditions.inputs.shaft_power_off_take   = None

    #link the high pressure turbine to the combustor
    hpt_conditions.inputs.stagnation_temperature    = combustor_conditions.outputs.stagnation_temperature
    hpt_conditions.inputs.stagnation_pressure       = combustor_conditions.outputs.stagnation_pressure
    hpt_conditions.inputs.fuel_to_air_ratio         = combustor_conditions.outputs.fuel_to_air_ratio

    #link the high pressuer turbine to the high pressure compressor
    hpt_conditions.inputs.compressor                = hpc_conditions.outputs

    #link the high pressure turbine to the fan
    hpt_conditions.inputs.fan                       = fan_conditions.outputs
    hpt_conditions.inputs.bypass_ratio              = 0.0 #set to zero to ensure that fan not linked here
    hpt_conditions.inputs.shaft_power_off_take      = None

    #flow through the high pressure turbine
    compute_turbine_performance(high_pressure_turbine,hpt_conditions, freestream)

    #link the low pressure turbine to the high pressure turbine
    lpt_conditions.inputs.stagnation_temperature     = hpt_conditions.outputs.stagnation_temperature
    lpt_conditions.inputs.stagnation_pressure        = hpt_conditions.outputs.stagnation_pressure

    #link the low pressure turbine to the low_pressure_compresor
    lpt_conditions.inputs.compressor                 = lpc_conditions.outputs

    #link the low pressure turbine to the combustor
    lpt_conditions.inputs.fuel_to_air_ratio          = combustor_conditions.outputs.fuel_to_air_ratio

    #link the low pressure turbine to the fan
    lpt_conditions.inputs.fan                        = fan_conditions.outputs 

    #get the bypass ratio from the thrust component
    lpt_conditions.inputs.bypass_ratio               = bypass_ratio

    #flow through the low pressure turbine
    compute_turbine_performance(low_pressure_turbine,lpt_conditions, freestream)

    #link the core nozzle to the low pressure turbine
    core_nozzle_conditions.inputs.stagnation_temperature              = lpt_conditions.outputs.stagnation_temperature
    core_nozzle_conditions.inputs.stagnation_pressure                 = lpt_conditions.outputs.stagnation_pressure

    #flow through the core nozzle
    compute_expansion_nozzle_performance(core_nozzle,core_nozzle_conditions,freestream)

    #link the dan nozzle to the fan
    fan_nozzle_conditions.inputs.stagnation_temperature               = fan_conditions.outputs.stagnation_temperature
    fan_nozzle_conditions.inputs.stagnation_pressure                  = fan_conditions.outputs.stagnation_pressure

    # flow through the fan nozzle
    compute_expansion_nozzle_performance(fan_nozzle,fan_nozzle_conditions, freestream)

    # compute the thrust using the thrust component
    #link the thrust component to the fan nozzle
    turbofan_conditions.fan_exit_velocity                        = fan_nozzle_conditions.outputs.velocity
    turbofan_conditions.fan_area_ratio                           = fan_nozzle_conditions.outputs.area_ratio
    turbofan_conditions.fan_nozzle                               = fan_nozzle_conditions.outputs

    #link the thrust component to the core nozzle
    turbofan_conditions.core_exit_velocity                       = core_nozzle_conditions.outputs.velocity
    turbofan_conditions.core_area_ratio                          = core_nozzle_conditions.outputs.area_ratio
    turbofan_conditions.core_nozzle                              = core_nozzle_conditions.outputs

    #link the thrust component to the combustor
    turbofan_conditions.fuel_to_air_ratio                        = combustor_conditions.outputs.fuel_to_air_ratio

    #link the thrust component to the low pressure compressor 
    turbofan_conditions.total_temperature_reference              = lpc_conditions.outputs.stagnation_temperature
    turbofan_conditions.total_pressure_reference                 = lpc_conditions.outputs.stagnation_pressure 
    turbofan_conditions.bypass_ratio                             = bypass_ratio
    turbofan_conditions.flow_through_core                        = 1./(1.+bypass_ratio) #scaled constant to turn on core thrust computation
    turbofan_conditions.flow_through_fan                         = bypass_ratio/(1.+bypass_ratio) #scaled constant to turn on fan thrust computation        

    # compute the thrust
    compute_thrust(turbofan,turbofan_conditions,freestream)

    # getting the network outputs
    moment_vector      = 0*state.ones_row(3)
    F                  = 0*state.ones_row(3)
    F[:,0]             =  turbofan_conditions.thrust[:,0]
    moment_vector[:,0] =  turbofan.origin[0][0] -   center_of_gravity[0][0] 
    moment_vector[:,1] =  turbofan.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2] =  turbofan.origin[0][2]  -  center_of_gravity[0][2]
    M                  =  rp.cross(moment_vector, F)   
    total_moment       += M 
    total_power        += turbofan_conditions.power
    total_thrust       += F

    # store data
    core_nozzle_res = Data(
                exit_static_temperature             = core_nozzle_conditions.outputs.static_temperature,
                exit_static_pressure                = core_nozzle_conditions.outputs.static_pressure,
                exit_stagnation_temperature         = core_nozzle_conditions.outputs.stagnation_temperature,
                exit_stagnation_pressure            = core_nozzle_conditions.outputs.static_pressure,
                exit_velocity                       = core_nozzle_conditions.outputs.velocity
            )

    fan_nozzle_res = Data(
                exit_static_temperature             = fan_nozzle_conditions.outputs.static_temperature,
                exit_static_pressure                = fan_nozzle_conditions.outputs.static_pressure,
                exit_stagnation_temperature         = fan_nozzle_conditions.outputs.stagnation_temperature,
                exit_stagnation_pressure            = fan_nozzle_conditions.outputs.static_pressure,
                exit_velocity                       = fan_nozzle_conditions.outputs.velocity
            )

    noise_conditions.turbofan.fan_nozzle    = fan_nozzle_res
    noise_conditions.turbofan.core_nozzle   = core_nozzle_res  
    noise_conditions.turbofan.fan           = None
    stored_results_flag                  = True
    stored_propulsor_tag                 = turbofan.tag 
    
    return total_thrust,total_moment,total_power,stored_results_flag,stored_propulsor_tag
    
    
    
def reuse_stored_data(state,fuel_line,turbofan,stored_propulsor_tag,total_thrust,total_moment,total_power,center_of_gravity):
    '''Reuses results from one turbofan for identical turbofans
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure   [-]  
    fuel_line            - fuelline                              [-] 
    turbofan            - turbofan data structure                [-] 
    total_thrust         - thrust of turbofan group              [N]
    total_power          - power of turbofan group               [W] 

    Outputs:  
    total_thrust         - thrust of turbofan group              [N]
    total_power          - power of turbofan group               [W] 
    
    Properties Used: 
    N.A.        
    ''' 
    conditions                              = state.conditions  
    turbofan_conditions_0                   = conditions.energy[fuel_line.tag][stored_propulsor_tag]
    noise_conditions_0                      = conditions.noise[fuel_line.tag][stored_propulsor_tag] 
    turbofan_conditions                     = conditions.energy[fuel_line.tag][turbofan.tag]  
    noise_conditions                        = conditions.noise[fuel_line.tag][turbofan.tag]
    
    # compute moment  
    moment_vector      = 0*state.ones_row(3)
    F                  = 0*state.ones_row(3)
    F[:,0]             = turbofan_conditions_0.thrust[:,0] 
    moment_vector[:,0] = turbofan.origin[0][0] -   center_of_gravity[0][0] 
    moment_vector[:,1] = turbofan.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2] = turbofan.origin[0][2]  -  center_of_gravity[0][2]
    M                  = rp.cross(moment_vector, F)          
    
    turbofan_conditions.throttle            = turbofan_conditions_0.throttle
    turbofan_conditions.thrust              = turbofan_conditions_0.thrust   
    turbofan_conditions.power               = turbofan_conditions_0.power  
    turbofan_conditions.fuel_flow_rate      = turbofan_conditions_0.fuel_flow_rate 
    noise_conditions.turbofan.fan_nozzle    = noise_conditions_0.turbofan.fan_nozzle 
    noise_conditions.turbofan.core_nozzle   = noise_conditions_0.turbofan.core_nozzle 
    noise_conditions.turbofan.fan           = None   
    total_moment                           += M
    total_power                            += turbofan_conditions.power
    total_thrust                           += turbofan_conditions.thrust 
 
    return total_thrust,total_moment,total_power    