## @ingroup Methods-Energy-Propulsors-Turbofan_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Turbofan_Propulsor/compute_turbofan_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke

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

# ----------------------------------------------------------------------------------------------------------------------
# compute_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsors-Turbofan_Propulsor
def compute_turbofan_performance(fuel_line,state):  
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
    conditions      = state.conditions
    stored_results_flag  = False  
    
    for turbofan in fuel_line.propulsors:  
        if turbofan.active == True:  
            if fuel_line.identical_propulsors == False:
                # run analysis  
                total_thrust,total_power ,stored_results_flag,stored_propulsor_tag = compute_performance(conditions,fuel_line,turbofan,total_thrust,total_power)
            else:             
                if stored_results_flag == False: 
                    # run analysis 
                    total_thrust,total_power ,stored_results_flag,stored_propulsor_tag = compute_performance(conditions,fuel_line,turbofan,total_thrust,total_power)
                else:
                    # use old results 
                    total_thrust,total_power  = reuse_stored_data(conditions,fuel_line,turbofan,stored_propulsor_tag,total_thrust,total_power)
                
    return total_thrust,total_power

def compute_performance(conditions,fuel_line,turbofan,total_thrust,total_power):  
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
    noise_results             = conditions.noise.distribution_lines[fuel_line.tag].propulsors[turbofan.tag] 
    turbofan_results          = conditions.energy.distribution_lines[fuel_line.tag].propulsors[turbofan.tag] 
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
    compute_ram_performance(ram,conditions)

    #link inlet nozzle to ram 
    inlet_nozzle.inputs.stagnation_temperature             = ram.outputs.stagnation_temperature 
    inlet_nozzle.inputs.stagnation_pressure                = ram.outputs.stagnation_pressure

    #Flow through the inlet nozzle
    compute_compression_nozzle_performance(inlet_nozzle,conditions)

    #--link low pressure compressor to the inlet nozzle
    low_pressure_compressor.inputs.stagnation_temperature  = inlet_nozzle.outputs.stagnation_temperature
    low_pressure_compressor.inputs.stagnation_pressure     = inlet_nozzle.outputs.stagnation_pressure

    #Flow through the low pressure compressor
    compute_compressor_performance(low_pressure_compressor,conditions)

    #link the high pressure compressor to the low pressure compressor
    high_pressure_compressor.inputs.stagnation_temperature = low_pressure_compressor.outputs.stagnation_temperature
    high_pressure_compressor.inputs.stagnation_pressure    = low_pressure_compressor.outputs.stagnation_pressure

    #Flow through the high pressure compressor
    compute_compressor_performance(high_pressure_compressor,conditions)

    #Link the fan to the inlet nozzle
    fan.inputs.stagnation_temperature                      = inlet_nozzle.outputs.stagnation_temperature
    fan.inputs.stagnation_pressure                         = inlet_nozzle.outputs.stagnation_pressure

    #flow through the fan
    compute_fan_performance(fan,conditions)

    #link the combustor to the high pressure compressor
    combustor.inputs.stagnation_temperature                = high_pressure_compressor.outputs.stagnation_temperature
    combustor.inputs.stagnation_pressure                   = high_pressure_compressor.outputs.stagnation_pressure

    #flow through the high pressor comprresor
    compute_combustor_performance(combustor,conditions)

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
    compute_turbine_performance(high_pressure_turbine,conditions)

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
    compute_turbine_performance(low_pressure_turbine,conditions)

    #link the core nozzle to the low pressure turbine
    core_nozzle.inputs.stagnation_temperature              = low_pressure_turbine.outputs.stagnation_temperature
    core_nozzle.inputs.stagnation_pressure                 = low_pressure_turbine.outputs.stagnation_pressure

    #flow through the core nozzle
    compute_expansion_nozzle_performance(core_nozzle,conditions)

    #link the dan nozzle to the fan
    fan_nozzle.inputs.stagnation_temperature               = fan.outputs.stagnation_temperature
    fan_nozzle.inputs.stagnation_pressure                  = fan.outputs.stagnation_pressure

    # flow through the fan nozzle
    compute_expansion_nozzle_performance(fan_nozzle,conditions)

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

    # compute the thrust
    compute_thrust(turbofan,conditions,throttle = turbofan_results.throttle )

    # getting the network outputs from the thrust outputs   
    turbofan_results.thrust          = turbofan.outputs.thrust
    turbofan_results.power           = turbofan.outputs.power  
    turbofan_results.fuel_flow_rate  = turbofan.outputs.fuel_flow_rate 
    total_power                     += turbofan_results.power
    total_thrust[:,0]               += turbofan_results.thrust[:,0]

    # store data
    core_nozzle_res = Data(
                exit_static_temperature             = core_nozzle.outputs.static_temperature,
                exit_static_pressure                = core_nozzle.outputs.static_pressure,
                exit_stagnation_temperature         = core_nozzle.outputs.stagnation_temperature,
                exit_stagnation_pressure            = core_nozzle.outputs.static_pressure,
                exit_velocity                       = core_nozzle.outputs.velocity
            )

    fan_nozzle_res = Data(
                exit_static_temperature             = fan_nozzle.outputs.static_temperature,
                exit_static_pressure                = fan_nozzle.outputs.static_pressure,
                exit_stagnation_temperature         = fan_nozzle.outputs.stagnation_temperature,
                exit_stagnation_pressure            = fan_nozzle.outputs.static_pressure,
                exit_velocity                       = fan_nozzle.outputs.velocity
            )

    noise_results.turbofan.fan_nozzle    = fan_nozzle_res
    noise_results.turbofan.core_nozzle   = core_nozzle_res  
    noise_results.turbofan.fan           = None
    stored_results_flag                  = True
    stored_propulsor_tag                 = turbofan.tag 
    
    return total_thrust,total_power ,stored_results_flag,stored_propulsor_tag
    
    
    
def reuse_stored_data(conditions,fuel_line,turbofan,stored_propulsor_tag,total_thrust,total_power):
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
    turbofan_results_0                   = conditions.energy.distribution_lines[fuel_line.tag].propulsors[stored_propulsor_tag]
    noise_results_0                      = conditions.noise.distribution_lines[fuel_line.tag].propulsors[stored_propulsor_tag] 
    turbofan_results                     = conditions.energy.distribution_lines[fuel_line.tag].propulsors[turbofan.tag]  
    noise_results                        = conditions.noise.distribution_lines[fuel_line.tag].propulsors[turbofan.tag]
    turbofan_results.throttle            = turbofan_results_0.throttle
    turbofan_results.thrust              = turbofan_results_0.thrust   
    turbofan_results.power               = turbofan_results_0.power  
    turbofan_results.fuel_flow_rate      = turbofan_results_0.fuel_flow_rate 
    noise_results.turbofan.fan_nozzle    = noise_results_0.turbofan.fan_nozzle 
    noise_results.turbofan.core_nozzle   = noise_results_0.turbofan.core_nozzle 
    noise_results.turbofan.fan           = None   
    total_power                          += turbofan_results.power
    total_thrust[:,0]                    += turbofan_results.thrust[:,0] 
 
    return total_thrust,total_power    