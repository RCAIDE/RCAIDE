# RCAIDE/Library/Methods/Propulsors/Turbofan_Propulsor/design_turbofan.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE Imports
import RCAIDE
from RCAIDE.Framework.Mission.Common                                 import Conditions
from RCAIDE.Library.Methods.Propulsors.Converters.Ram                import compute_ram_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Combustor          import compute_combustor_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Compressor         import compute_compressor_performance 
from RCAIDE.Library.Methods.Propulsors.Converters.Fan                import compute_fan_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Turbine            import compute_turbine_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Expansion_Nozzle   import compute_expansion_nozzle_performance 
from RCAIDE.Library.Methods.Propulsors.Converters.Compression_Nozzle import compute_compression_nozzle_performance
from RCAIDE.Library.Methods.Propulsors.Turbofan_Propulsor            import size_core
from RCAIDE.Library.Methods.Propulsors.Common                        import compute_static_sea_level_performance


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
    
    turbofan_conditions                                         = Conditions() 
    turbofan_conditions[combustor.tag]                          = Conditions() 
    turbofan_conditions[combustor.tag].inputs                   = Conditions() 
    turbofan_conditions[combustor.tag].outputs                  = Conditions() 
    turbofan_conditions[combustor.tag].inputs.nondim_mass_ratio = np.array([[1.0]])  
    turbofan_conditions[ram.tag]                                = Conditions() 
    turbofan_conditions[ram.tag].inputs                         = Conditions() 
    turbofan_conditions[ram.tag].outputs                        = Conditions() 
    turbofan_conditions[fan.tag]                                = Conditions() 
    turbofan_conditions[fan.tag].inputs                         = Conditions() 
    turbofan_conditions[fan.tag].outputs                        = Conditions() 
    turbofan_conditions[high_pressure_compressor.tag]           = Conditions()
    turbofan_conditions[high_pressure_compressor.tag].inputs    = Conditions()
    turbofan_conditions[high_pressure_compressor.tag].outputs   = Conditions()
    turbofan_conditions[low_pressure_compressor.tag]            = Conditions()
    turbofan_conditions[low_pressure_compressor.tag].inputs     = Conditions()
    turbofan_conditions[low_pressure_compressor.tag].outputs    = Conditions()
    turbofan_conditions[high_pressure_turbine.tag]              = Conditions()
    turbofan_conditions[high_pressure_turbine.tag].inputs       = Conditions()
    turbofan_conditions[high_pressure_turbine.tag].outputs      = Conditions()
    turbofan_conditions[low_pressure_turbine.tag]               = Conditions()
    turbofan_conditions[low_pressure_turbine.tag].inputs        = Conditions()
    turbofan_conditions[low_pressure_turbine.tag].outputs       = Conditions()
    turbofan_conditions[core_nozzle.tag]                        = Conditions()
    turbofan_conditions[core_nozzle.tag].inputs                 = Conditions()
    turbofan_conditions[core_nozzle.tag].outputs                = Conditions()
    turbofan_conditions[fan_nozzle.tag]                         = Conditions()
    turbofan_conditions[fan_nozzle.tag].inputs                  = Conditions()
    turbofan_conditions[fan_nozzle.tag].outputs                 = Conditions()
    turbofan_conditions[inlet_nozzle.tag]                       = Conditions()
    turbofan_conditions[inlet_nozzle.tag].inputs                = Conditions()
    turbofan_conditions[inlet_nozzle.tag].outputs               = Conditions()
    turbofan_conditions.inputs                                  = Conditions()
    turbofan_conditions.outputs                                 = Conditions()

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
     
    # Step 1: Set the working fluid to determine the fluid properties
    ram.working_fluid                             = turbofan.working_fluid
    
    # Step 2: Compute flow through the ram , this computes the necessary flow quantities and stores it into conditions
    compute_ram_performance(ram,ram_conditions, freestream)
    
    # Step 3: link inlet nozzle to ram 
    inlet_nozzle_conditions.inputs.stagnation_temperature             = ram_conditions.outputs.stagnation_temperature
    inlet_nozzle_conditions.inputs.stagnation_pressure                = ram_conditions.outputs.stagnation_pressure
    
    # Step 4: Compute flow through the inlet nozzle
    compute_compression_nozzle_performance(inlet_nozzle,inlet_nozzle_conditions, freestream)      
                    
    # Step 5: Link low pressure compressor to the inlet nozzle
    lpc_conditions.inputs.stagnation_temperature  = inlet_nozzle_conditions.outputs.stagnation_temperature
    lpc_conditions.inputs.stagnation_pressure     = inlet_nozzle_conditions.outputs.stagnation_pressure
    
    # Step 6: Compute flow through the low pressure compressor
    compute_compressor_performance(low_pressure_compressor,lpc_conditions, freestream)
    
    # Step 7: Link the high pressure compressor to the low pressure compressor
    hpc_conditions.inputs.stagnation_temperature = lpc_conditions.outputs.stagnation_temperature
    hpc_conditions.inputs.stagnation_pressure    = lpc_conditions.outputs.stagnation_pressure
    
    # Step 8: Compute flow through the high pressure compressor
    compute_compressor_performance(high_pressure_compressor,hpc_conditions, freestream)
    
    # Step 9: Link the fan to the inlet nozzle
    fan_conditions.inputs.stagnation_temperature                      = inlet_nozzle_conditions.outputs.stagnation_temperature
    fan_conditions.inputs.stagnation_pressure                         = inlet_nozzle_conditions.outputs.stagnation_pressure
    
    # Step 10: Compute flow through the fan
    compute_fan_performance(fan,fan_conditions, freestream)
    
    # Step 11: Link the combustor to the high pressure compressor
    combustor_conditions.inputs.stagnation_temperature                = hpc_conditions.outputs.stagnation_temperature
    combustor_conditions.inputs.stagnation_pressure                   = hpc_conditions.outputs.stagnation_pressure
    
    # Step 12: Compute flow through the high pressor comprresor
    compute_combustor_performance(combustor,combustor_conditions, freestream)
    
    # Step 13: Link the high pressure turbione to the combustor
    hpt_conditions.inputs.stagnation_temperature    = combustor_conditions.outputs.stagnation_temperature
    hpt_conditions.inputs.stagnation_pressure       = combustor_conditions.outputs.stagnation_pressure
    hpt_conditions.inputs.fuel_to_air_ratio         = combustor_conditions.outputs.fuel_to_air_ratio
    
    # Step 14: Link the high pressure turbine to the high pressure compressor
    hpt_conditions.inputs.compressor                = hpc_conditions.outputs
    
    # Step 15 Link the high pressure turbine to the fan
    hpt_conditions.inputs.fan                       = fan_conditions.outputs
    hpt_conditions.inputs.bypass_ratio              = 0.0 #set to zero to ensure that fan not linked here
    hpt_conditions.inputs.shaft_power_off_take      = None
    
    # Step 16L Compute flow through the high pressure turbine
    compute_turbine_performance(high_pressure_turbine,hpt_conditions, freestream)
            
    # Step 17: Link the low pressure turbine to the high pressure turbine
    lpt_conditions.inputs.stagnation_temperature     = hpt_conditions.outputs.stagnation_temperature
    lpt_conditions.inputs.stagnation_pressure        = hpt_conditions.outputs.stagnation_pressure
    
    # Step 18: Link the low pressure turbine to the low_pressure_compresor
    lpt_conditions.inputs.compressor                 = lpc_conditions.outputs
    
    # Step 19: Link the low pressure turbine to the combustor
    lpt_conditions.inputs.fuel_to_air_ratio          = combustor_conditions.outputs.fuel_to_air_ratio
    
    # Step 20: Link the low pressure turbine to the fan
    lpt_conditions.inputs.fan                        =  fan_conditions.outputs 
    lpt_conditions.inputs.bypass_ratio               =  bypass_ratio
    lpt_conditions.inputs.shaft_power_off_take       = None
    
    # Step 21: Compute flow through the low pressure turbine
    compute_turbine_performance(low_pressure_turbine,lpt_conditions, freestream)
    
    # Step 22: Link the core nozzle to the low pressure turbine
    core_nozzle_conditions.inputs.stagnation_temperature              = lpt_conditions.outputs.stagnation_temperature
    core_nozzle_conditions.inputs.stagnation_pressure                 = lpt_conditions.outputs.stagnation_pressure
    
    # Step 23: Compute flow through the core nozzle
    compute_expansion_nozzle_performance(core_nozzle,core_nozzle_conditions, freestream)
   
    # Step 24: Link the fan nozzle to the fan
    fan_nozzle_conditions.inputs.stagnation_temperature               = fan_conditions.outputs.stagnation_temperature
    fan_nozzle_conditions.inputs.stagnation_pressure                  = fan_conditions.outputs.stagnation_pressure
    
    # Step 25: Compute flow through the fan nozzle
    compute_expansion_nozzle_performance(fan_nozzle,fan_nozzle_conditions, freestream)
     
    # Step 26: Link the turbofan to outputs from various compoments    
    turbofan_conditions.bypass_ratio                             = bypass_ratio
    turbofan_conditions.flow_through_core                        =  1./(1.+bypass_ratio) #scaled constant to turn on core thrust computation
    turbofan_conditions.flow_through_fan                         =  bypass_ratio/(1.+bypass_ratio) #scaled constant to turn on fan thrust computation
    
    # Fan Nozzle 
    turbofan_conditions.fan_exit_velocity                        = fan_nozzle_conditions.outputs.velocity
    turbofan_conditions.fan_area_ratio                           = fan_nozzle_conditions.outputs.area_ratio
    turbofan_conditions.fan_nozzle                               = fan_nozzle_conditions.outputs
    
    # Core Nozzle 
    turbofan_conditions.core_exit_velocity                       = core_nozzle_conditions.outputs.velocity
    turbofan_conditions.core_area_ratio                          = core_nozzle_conditions.outputs.area_ratio
    turbofan_conditions.core_nozzle                              = core_nozzle_conditions.outputs
    
    # Combustor 
    turbofan_conditions.fuel_to_air_ratio                        = combustor_conditions.outputs.fuel_to_air_ratio
    
    # Low Pressure 
    turbofan_conditions.total_temperature_reference              = lpc_conditions.outputs.stagnation_temperature
    turbofan_conditions.total_pressure_reference                 = lpc_conditions.outputs.stagnation_pressure    

    # Step 27: Size the core of the turbofan  
    size_core(turbofan,turbofan_conditions, freestream)
    
    # Step 28: Static Sea Level Thrust 
    compute_static_sea_level_performance(turbofan)
     
    return 