# RCAIDE/Library/Methods/Energy/Propulsors/Turbofan_Propulsor/design_turbofan.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE Imports
import RCAIDE
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Ram                import compute_ram_performance
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Combustor          import compute_combustor_performance
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Compressor         import compute_compressor_performance 
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Fan                import compute_fan_performance
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Turbine            import compute_turbine_performance
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Expansion_Nozzle   import compute_expansion_nozzle_performance 
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Compression_Nozzle import compute_compression_nozzle_performance
from RCAIDE.Library.Methods.Energy.Propulsors.Turbofan_Propulsor            import size_core
from RCAIDE.Library.Methods.Energy.Propulsors.Common                        import compute_static_sea_level_performance


# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Design Turbofan
# ---------------------------------------------------------------------------------------------------------------------- 
def design_turbofan(turbofan):
    """Compute perfomance properties of a turbofan based on polytropic ration and combustor properties.
    Turbofan is created by manually linking the different components
    
    
    Assumtions:
       None 
    
    Source:
    
    Args:
        turbofan (dict): turbofan data structure [-]
    
    Returns:
        None 
    
    """
    # check if mach number and temperature are passed
    if(turbofan.design_mach_number==None) and (turbofan.design_altitude==None): 
        raise NameError('The sizing conditions require an altitude and a Mach number') 
    else:
        #call the atmospheric model to get the conditions at the specified altitude
        atmosphere = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
        atmo_data  = atmosphere.compute_values(turbofan.design_altitude,turbofan.design_isa_deviation)
        planet     = RCAIDE.Library.Attributes.Planets.Earth()
        
        p   = atmo_data.pressure          
        T   = atmo_data.temperature       
        rho = atmo_data.density          
        a   = atmo_data.speed_of_sound    
        mu  = atmo_data.dynamic_viscosity           
    
        # setup conditions
        conditions = RCAIDE.Framework.Mission.Common.Results()
    
        # freestream conditions    
        conditions.freestream.altitude                    = np.atleast_1d(turbofan.design_altitude)
        conditions.freestream.mach_number                 = np.atleast_1d(turbofan.design_mach_number)
        conditions.freestream.pressure                    = np.atleast_1d(p)
        conditions.freestream.temperature                 = np.atleast_1d(T)
        conditions.freestream.density                     = np.atleast_1d(rho)
        conditions.freestream.dynamic_viscosity           = np.atleast_1d(mu)
        conditions.freestream.gravity                     = np.atleast_1d(planet.compute_gravity(turbofan.design_altitude))
        conditions.freestream.isentropic_expansion_factor = np.atleast_1d(turbofan.working_fluid.compute_gamma(T,p))
        conditions.freestream.Cp                          = np.atleast_1d(turbofan.working_fluid.compute_cp(T,p))
        conditions.freestream.R                           = np.atleast_1d(turbofan.working_fluid.gas_specific_constant)
        conditions.freestream.speed_of_sound              = np.atleast_1d(a)
        conditions.freestream.velocity                    = np.atleast_1d(a*turbofan.design_mach_number) 
    
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
    
    # Step 1: Set the working fluid to determine the fluid properties
    ram.inputs.working_fluid                             = turbofan.working_fluid
    
    # Step 2: Compute flow through the ram , this computes the necessary flow quantities and stores it into conditions
    compute_ram_performance(ram,conditions)
    
    # Step 3: link inlet nozzle to ram 
    inlet_nozzle.inputs.stagnation_temperature             = ram.outputs.stagnation_temperature
    inlet_nozzle.inputs.stagnation_pressure                = ram.outputs.stagnation_pressure
    
    # Step 4: Compute flow through the inlet nozzle
    compute_compression_nozzle_performance(inlet_nozzle,conditions)      
                    
    # Step 5: Link low pressure compressor to the inlet nozzle
    low_pressure_compressor.inputs.stagnation_temperature  = inlet_nozzle.outputs.stagnation_temperature
    low_pressure_compressor.inputs.stagnation_pressure     = inlet_nozzle.outputs.stagnation_pressure
    
    # Step 6: Compute flow through the low pressure compressor
    compute_compressor_performance(low_pressure_compressor,conditions)
    
    # Step 7: Link the high pressure compressor to the low pressure compressor
    high_pressure_compressor.inputs.stagnation_temperature = low_pressure_compressor.outputs.stagnation_temperature
    high_pressure_compressor.inputs.stagnation_pressure    = low_pressure_compressor.outputs.stagnation_pressure
    
    # Step 8: Compute flow through the high pressure compressor
    compute_compressor_performance(high_pressure_compressor,conditions)
    
    # Step 9: Link the fan to the inlet nozzle
    fan.inputs.stagnation_temperature                      = inlet_nozzle.outputs.stagnation_temperature
    fan.inputs.stagnation_pressure                         = inlet_nozzle.outputs.stagnation_pressure
    
    # Step 10: Compute flow through the fan
    compute_fan_performance(fan,conditions)
    
    # Step 11: Link the combustor to the high pressure compressor
    combustor.inputs.stagnation_temperature                = high_pressure_compressor.outputs.stagnation_temperature
    combustor.inputs.stagnation_pressure                   = high_pressure_compressor.outputs.stagnation_pressure
    
    # Step 12: Compute flow through the high pressor comprresor
    compute_combustor_performance(combustor,conditions)
    
    # Step 13: Link the high pressure turbione to the combustor
    high_pressure_turbine.inputs.stagnation_temperature    = combustor.outputs.stagnation_temperature
    high_pressure_turbine.inputs.stagnation_pressure       = combustor.outputs.stagnation_pressure
    high_pressure_turbine.inputs.fuel_to_air_ratio         = combustor.outputs.fuel_to_air_ratio
    
    # Step 14: Link the high pressure turbine to the high pressure compressor
    high_pressure_turbine.inputs.compressor                = high_pressure_compressor.outputs
    
    # Step 15 Link the high pressure turbine to the fan
    high_pressure_turbine.inputs.fan                       = fan.outputs
    high_pressure_turbine.inputs.bypass_ratio              = 0.0 #set to zero to ensure that fan not linked here
    
    # Step 16L Compute flow through the high pressure turbine
    compute_turbine_performance(high_pressure_turbine,conditions)
            
    # Step 17: Link the low pressure turbine to the high pressure turbine
    low_pressure_turbine.inputs.stagnation_temperature     = high_pressure_turbine.outputs.stagnation_temperature
    low_pressure_turbine.inputs.stagnation_pressure        = high_pressure_turbine.outputs.stagnation_pressure
    
    # Step 18: Link the low pressure turbine to the low_pressure_compresor
    low_pressure_turbine.inputs.compressor                 = low_pressure_compressor.outputs
    
    # Step 19: Link the low pressure turbine to the combustor
    low_pressure_turbine.inputs.fuel_to_air_ratio          = combustor.outputs.fuel_to_air_ratio
    
    # Step 20: Link the low pressure turbine to the fan
    low_pressure_turbine.inputs.fan                        =  fan.outputs 
    low_pressure_turbine.inputs.bypass_ratio               =  bypass_ratio
    
    # Step 21: Compute flow through the low pressure turbine
    compute_turbine_performance(low_pressure_turbine,conditions)
    
    # Step 22: Link the core nozzle to the low pressure turbine
    core_nozzle.inputs.stagnation_temperature              = low_pressure_turbine.outputs.stagnation_temperature
    core_nozzle.inputs.stagnation_pressure                 = low_pressure_turbine.outputs.stagnation_pressure
    
    # Step 23: Compute flow through the core nozzle
    compute_expansion_nozzle_performance(core_nozzle,conditions)
   
    # Step 24: Link the fan nozzle to the fan
    fan_nozzle.inputs.stagnation_temperature               = fan.outputs.stagnation_temperature
    fan_nozzle.inputs.stagnation_pressure                  = fan.outputs.stagnation_pressure
    
    # Step 25: Compute flow through the fan nozzle
    compute_expansion_nozzle_performance(fan_nozzle,conditions)
     
    # Step 26: Link the turbofan to outputs from various compoments    
    turbofan.inputs.bypass_ratio                             = bypass_ratio
    turbofan.inputs.flow_through_core                        =  1./(1.+bypass_ratio) #scaled constant to turn on core thrust computation
    turbofan.inputs.flow_through_fan                         =  bypass_ratio/(1.+bypass_ratio) #scaled constant to turn on fan thrust computation
    
    # Fan Nozzle 
    turbofan.inputs.fan_exit_velocity                        = fan_nozzle.outputs.velocity
    turbofan.inputs.fan_area_ratio                           = fan_nozzle.outputs.area_ratio
    turbofan.inputs.fan_nozzle                               = fan_nozzle.outputs
    
    # Core Nozzle 
    turbofan.inputs.core_exit_velocity                       = core_nozzle.outputs.velocity
    turbofan.inputs.core_area_ratio                          = core_nozzle.outputs.area_ratio
    turbofan.inputs.core_nozzle                              = core_nozzle.outputs
    
    # Combustor 
    turbofan.inputs.fuel_to_air_ratio                        = combustor.outputs.fuel_to_air_ratio
    
    # Low Pressure 
    turbofan.inputs.total_temperature_reference              = low_pressure_compressor.outputs.stagnation_temperature
    turbofan.inputs.total_pressure_reference                 = low_pressure_compressor.outputs.stagnation_pressure    

    # Step 27: Size the core of the turbofan  
    size_core(turbofan,conditions)
    
    # Step 28: Static Sea Level Thrust 
    compute_static_sea_level_performance(turbofan)
     
    return 