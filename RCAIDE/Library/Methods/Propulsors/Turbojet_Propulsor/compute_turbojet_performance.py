## @ingroup Methods-Energy-Propulsors-Networks-Turbojet_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Networks/Turbojet_Propulsor/compute_turbojet_performance.py
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
from RCAIDE.Library.Methods.Propulsors.Converters.Turbine            import compute_turbine_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Supersonic_Nozzle  import compute_supersonic_nozzle_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Compression_Nozzle import compute_compression_nozzle_performance
from RCAIDE.Library.Methods.Propulsors.Turbojet_Propulsor            import compute_thrust
import  numpy as  np 
# ----------------------------------------------------------------------------------------------------------------------
# compute_turbojet_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsors-Turbojet_Propulsor
def compute_turbojet_performance(turbojet,state,fuel_line,center_of_gravity= [[0.0, 0.0,0.0]]):  
    ''' Computes the perfomrance of one turbojet
    
    Assumptions: 
    N/A

    Source:
    N/A
    
    Inputs:  
    turbofan             - turbofan data structure               [-]  
    state                - operating conditions data structure   [-]  
    fuel_line            - fuelline                              [-]
    center_of_gravity    - aircraft center of gravity            [m]

    Outputs:  
    total_thrust         - thrust of turbofan group              [N]
    total_momnet         - moment of turbofan group              [Nm]
    total_power          - power of turbofan group               [W] 
    stored_results_flag  - boolean for stored results            [-]     
    stored_propulsor_tag - name of turbojet with stored results  [-]
    
    Properties Used: 
    N.A.          
    ''' 
    conditions                = state.conditions
    noise_conditions          = conditions.noise[fuel_line.tag][turbojet.tag]  
    turbojet_conditions       = conditions.energy[fuel_line.tag][turbojet.tag]  
    ram                       = turbojet.ram
    inlet_nozzle              = turbojet.inlet_nozzle
    low_pressure_compressor   = turbojet.low_pressure_compressor
    high_pressure_compressor  = turbojet.high_pressure_compressor
    combustor                 = turbojet.combustor
    high_pressure_turbine     = turbojet.high_pressure_turbine
    low_pressure_turbine      = turbojet.low_pressure_turbine 
    afterburner               = turbojet.afterburner 
    core_nozzle               = turbojet.core_nozzle   

    # unpack component conditions 
    ram_conditions          = turbojet_conditions[ram.tag]     
    inlet_nozzle_conditions = turbojet_conditions[inlet_nozzle.tag]
    core_nozzle_conditions  = turbojet_conditions[core_nozzle.tag] 
    lpc_conditions          = turbojet_conditions[low_pressure_compressor.tag]
    hpc_conditions          = turbojet_conditions[high_pressure_compressor.tag]
    lpt_conditions          = turbojet_conditions[low_pressure_turbine.tag]
    hpt_conditions          = turbojet_conditions[high_pressure_turbine.tag]
    combustor_conditions    = turbojet_conditions[combustor.tag]
    afterburner_conditions  = turbojet_conditions[afterburner.tag] 
    
    # Set the working fluid to determine the fluid properties
    ram.working_fluid = turbojet.working_fluid

    # Flow through the ram , this computes the necessary flow quantities and stores it into conditions
    compute_ram_performance(ram,ram_conditions,conditions)

    # Link inlet nozzle to ram 
    inlet_nozzle_conditions.inputs.stagnation_temperature             = ram_conditions.outputs.stagnation_temperature 
    inlet_nozzle_conditions.inputs.stagnation_pressure                = ram_conditions.outputs.stagnation_pressure

    # Flow through the inlet nozzle
    compute_compression_nozzle_performance(inlet_nozzle,inlet_nozzle_conditions,conditions)

    # Link low pressure compressor to the inlet nozzle
    lpc_conditions.inputs.stagnation_temperature  = inlet_nozzle_conditions.outputs.stagnation_temperature
    lpc_conditions.inputs.stagnation_pressure     = inlet_nozzle_conditions.outputs.stagnation_pressure

    # Flow through the low pressure compressor
    compute_compressor_performance(low_pressure_compressor,lpc_conditions,conditions)

    # Link the high pressure compressor to the low pressure compressor
    hpc_conditions.inputs.stagnation_temperature = lpc_conditions.outputs.stagnation_temperature
    hpc_conditions.inputs.stagnation_pressure    = lpc_conditions.outputs.stagnation_pressure

    # Flow through the high pressure compressor
    compute_compressor_performance(high_pressure_compressor,hpc_conditions,conditions)

    # Link the combustor to the high pressure compressor
    combustor_conditions.inputs.stagnation_temperature                = hpc_conditions.outputs.stagnation_temperature
    combustor_conditions.inputs.stagnation_pressure                   = hpc_conditions.outputs.stagnation_pressure

    # Flow through the high pressor comprresor
    compute_combustor_performance(combustor,combustor_conditions,conditions) 

    # Link the high pressure turbine to the combustor
    hpt_conditions.inputs.stagnation_temperature    = combustor_conditions.outputs.stagnation_temperature
    hpt_conditions.inputs.stagnation_pressure       = combustor_conditions.outputs.stagnation_pressure
    hpt_conditions.inputs.fuel_to_air_ratio         = combustor_conditions.outputs.fuel_to_air_ratio 
    hpt_conditions.inputs.compressor                = hpc_conditions.outputs
    hpt_conditions.inputs.bypass_ratio              = 0.0

    # Flow through the high pressure turbine
    compute_turbine_performance(high_pressure_turbine,hpt_conditions,conditions)

    # Link the low pressure turbine to the high pressure turbine
    lpt_conditions.inputs.stagnation_temperature     = hpt_conditions.outputs.stagnation_temperature
    lpt_conditions.inputs.stagnation_pressure        = hpt_conditions.outputs.stagnation_pressure 
    lpt_conditions.inputs.compressor                 = lpc_conditions.outputs 
    lpt_conditions.inputs.fuel_to_air_ratio          = combustor_conditions.outputs.fuel_to_air_ratio 
    lpt_conditions.inputs.bypass_ratio               = 0.0

    # Flow through the low pressure turbine
    compute_turbine_performance(low_pressure_turbine,lpt_conditions,conditions)
 

    if turbojet.afterburner_active == True:
        #link the core nozzle to the afterburner
        afterburner_conditions.inputs.stagnation_temperature = lpt_conditions.outputs.stagnation_temperature
        afterburner_conditions.inputs.stagnation_pressure    = lpt_conditions.outputs.stagnation_pressure   
        afterburner_conditions.inputs.nondim_ratio           = 1.0 + combustor_conditions.outputs.fuel_to_air_ratio

        #flow through the afterburner
        compute_combustor_performance(afterburner,afterburner_conditions,conditions) 

        #link the core nozzle to the afterburner
        core_nozzle_conditions.inputs.stagnation_temperature              = afterburner_conditions.outputs.stagnation_temperature
        core_nozzle_conditions.inputs.stagnation_pressure                 = afterburner_conditions.outputs.stagnation_pressure   

    else:
        #link the core nozzle to the low pressure turbine
        core_nozzle_conditions.inputs.stagnation_temperature              = lpt_conditions.outputs.stagnation_temperature
        core_nozzle_conditions.inputs.stagnation_pressure                 = lpt_conditions.outputs.stagnation_pressure
 
    # Flow through the core nozzle
    compute_supersonic_nozzle_performance(core_nozzle,core_nozzle_conditions,conditions) 
 
    # Link the thrust component to the core nozzle 
    turbojet_conditions.core_nozzle_area_ratio                          = core_nozzle_conditions.outputs.area_ratio 
    turbojet_conditions.core_nozzle_static_pressure                     = core_nozzle_conditions.outputs.static_pressure
    turbojet_conditions.core_nozzle_exit_velocity                       = core_nozzle_conditions.outputs.velocity  

    # Link the thrust component to the combustor
    turbojet_conditions.fuel_to_air_ratio                        = combustor_conditions.outputs.fuel_to_air_ratio 
    if turbojet.afterburner_active == True:
        # previous fuel ratio is neglected when the afterburner fuel ratio is calculated
        turbojet_conditions.fuel_to_air_ratio += afterburner_conditions.outputs.fuel_to_air_ratio

    # Link the thrust component to the low pressure compressor 
    turbojet_conditions.total_temperature_reference              = lpc_conditions.outputs.stagnation_temperature
    turbojet_conditions.total_pressure_reference                 = lpc_conditions.outputs.stagnation_pressure 
    turbojet_conditions.flow_through_core                        = 1.0 #scaled constant to turn on core thrust computation  
    
    # Compute the thrust
    compute_thrust(turbojet,turbojet_conditions,conditions)
    
    # Compute forces and moments
    moment_vector      = 0*state.ones_row(3)
    F                  = 0*state.ones_row(3)
    F[:,0]             = turbojet_conditions.thrust[:,0]
    moment_vector[:,0] = turbojet.origin[0][0] -   center_of_gravity[0][0] 
    moment_vector[:,1] = turbojet.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2] = turbojet.origin[0][2]  -  center_of_gravity[0][2]
    M                  = np.cross(moment_vector, F)   
    moment             = M 
    power              = turbojet_conditions.power
    thrust             = F
 
    # store data
    core_nozzle_res = Data(
                exit_static_temperature             = core_nozzle_conditions.outputs.static_temperature,
                exit_static_pressure                = core_nozzle_conditions.outputs.static_pressure,
                exit_stagnation_temperature         = core_nozzle_conditions.outputs.stagnation_temperature,
                exit_stagnation_pressure            = core_nozzle_conditions.outputs.static_pressure,
                exit_velocity                       = core_nozzle_conditions.outputs.velocity
            ) 

    noise_conditions.turbojet.fan_nozzle    = None 
    noise_conditions.turbojet.core_nozzle   = core_nozzle_res
    noise_conditions.turbojet.fan           = None   
    stored_results_flag                     = True
    stored_propulsor_tag                    = turbojet.tag
    
    return thrust,moment,power,stored_results_flag,stored_propulsor_tag

def reuse_stored_turbojet_data(turbojet,state,fuel_line,stored_propulsor_tag,center_of_gravity= [[0.0, 0.0,0.0]]):
    '''Reuses results from one turbojet for identical propulsors
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    turbojet            - turbojet data structure                [-] 
    state               - operating conditions data structure   [-]  
    fuel_line            - fuelline                              [-] 
    total_thrust         - thrust of turbojet group              [N]
    total_power          - power of turbojet group               [W] 

    Outputs:  
    total_thrust         - thrust of turbojet group              [N]
    total_power          - power of turbojet group               [W] 
    
    Properties Used: 
    N.A.        
    ''' 
    conditions                              = state.conditions 
    turbojet_conditions_0                   = conditions.energy[fuel_line.tag][stored_propulsor_tag]
    noise_conditions_0                      = conditions.noise[fuel_line.tag][stored_propulsor_tag]  
    conditions.energy[fuel_line.tag][turbojet.tag]  = turbojet_conditions_0 
    conditions.noise[fuel_line.tag][turbojet.tag]   = noise_conditions_0
    
    # compute moment  
    moment_vector      = 0*state.ones_row(3)
    F                  = 0*state.ones_row(3)
    F[:,0]             = turbojet_conditions_0.thrust[:,0] 
    moment_vector[:,0] = turbojet.origin[0][0] -   center_of_gravity[0][0] 
    moment_vector[:,1] = turbojet.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2] = turbojet.origin[0][2]  -  center_of_gravity[0][2]
    moment             = np.cross(moment_vector, F)           
  
    power              = conditions.energy[fuel_line.tag][turbojet.tag].power
    thrust             = conditions.energy[fuel_line.tag][turbojet.tag].thrust 
    conditions.energy[fuel_line.tag][turbojet.tag].moment =  moment 
 
    return thrust,moment,power    