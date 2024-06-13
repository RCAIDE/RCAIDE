## @ingroup Methods-Energy-Propulsors-Turbojet_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Turbojet_Propulsor/design_turboshaft.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

# RCAIDE Imports     
import RCAIDE
from RCAIDE.Framework.Core                                                  import Data
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Ram                import compute_ram_performance
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Combustor          import compute_combustor_performance
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Compressor         import compute_compressor_performance
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Turbine            import compute_turbine_performance
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Expansion_Nozzle   import compute_expansion_nozzle_performance 
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Compression_Nozzle import compute_compression_nozzle_performance
from RCAIDE.Library.Methods.Energy.Propulsors.Turboshaft_Propulsor          import size_core, compute_power

# Python package imports   
import numpy                                                                as np

# ----------------------------------------------------------------------------------------------------------------------  
#  Design Turboshaft
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Methods-Energy-Propulsors-Turboshaft_Propulsor
def design_turboshaft(turboshaft):  
    #check if mach number and temperature are passed
    if(turboshaft.design_mach_number==None or turboshaft.design_altitude==None):
        
        #raise an error
        raise NameError('The sizing conditions require an altitude and a Mach number')
    
    else:
        #call the atmospheric model to get the conditions at the specified altitude
        atmosphere = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
        atmo_data  = atmosphere.compute_values(turboshaft.design_altitude,turboshaft.design_isa_deviation)
        planet     = RCAIDE.Library.Attributes.Planets.Earth()
        
        p   = atmo_data.pressure          
        T   = atmo_data.temperature       
        rho = atmo_data.density          
        a   = atmo_data.speed_of_sound    
        mu  = atmo_data.dynamic_viscosity   
    
        # setup conditions
        conditions = RCAIDE.Framework.Mission.Common.Results()
    
        # freestream conditions    
        conditions.freestream.altitude                    = np.atleast_1d(turboshaft.design_altitude)
        conditions.freestream.mach_number                 = np.atleast_1d(turboshaft.design_mach_number)
        conditions.freestream.pressure                    = np.atleast_1d(p)
        conditions.freestream.temperature                 = np.atleast_1d(T)
        conditions.freestream.density                     = np.atleast_1d(rho)
        conditions.freestream.dynamic_viscosity           = np.atleast_1d(mu)
        conditions.freestream.gravity                     = np.atleast_1d(planet.compute_gravity(turboshaft.design_altitude))
        conditions.freestream.isentropic_expansion_factor = np.atleast_1d(turboshaft.working_fluid.compute_gamma(T,p))
        conditions.freestream.Cp                          = np.atleast_1d(turboshaft.working_fluid.compute_cp(T,p))
        conditions.freestream.R                           = np.atleast_1d(turboshaft.working_fluid.gas_specific_constant)
        conditions.freestream.speed_of_sound              = np.atleast_1d(a)
        conditions.freestream.velocity                    = np.atleast_1d(a*turboshaft.design_mach_number)
         
    ram                                                   = turboshaft.ram
    inlet_nozzle                                          = turboshaft.inlet_nozzle
    compressor                                            = turboshaft.compressor
    combustor                                             = turboshaft.combustor
    high_pressure_turbine                                 = turboshaft.high_pressure_turbine
    low_pressure_turbine                                  = turboshaft.low_pressure_turbine
    core_nozzle                                           = turboshaft.core_nozzle  
    
    # Creating the network by manually linking the different components
    
    # set the working fluid to determine the fluid properties
    ram.inputs.working_fluid                              = turboshaft.working_fluid
    
     #Flow through the ram , this computes the necessary flow quantities and stores it into conditions
    compute_ram_performance(ram,conditions)
    
    # link inlet nozzle to ram 
    inlet_nozzle.inputs.stagnation_temperature            = ram.outputs.stagnation_temperature #conditions.freestream.stagnation_temperature
    inlet_nozzle.inputs.stagnation_pressure               = ram.outputs.stagnation_pressure    #conditions.freestream.stagnation_pressure
    
    # Flow through the inlet nozzle
    compute_compression_nozzle_performance(inlet_nozzle,conditions)
                    
    # link compressor to the inlet nozzle
    compressor.inputs.stagnation_temperature              = inlet_nozzle.outputs.stagnation_temperature
    compressor.inputs.stagnation_pressure                 = inlet_nozzle.outputs.stagnation_pressure
    
    # Flow through the compressor
    compute_compressor_performance(compressor,conditions)

    # link the combustor to the compressor
    combustor.inputs.stagnation_temperature               = compressor.outputs.stagnation_temperature
    combustor.inputs.stagnation_pressure                  = compressor.outputs.stagnation_pressure
    
    # flow through the combustor
    compute_combustor_performance(combustor,conditions)

    #link the high pressure turbione to the combustor
    high_pressure_turbine.inputs.stagnation_temperature   = combustor.outputs.stagnation_temperature
    high_pressure_turbine.inputs.stagnation_pressure      = combustor.outputs.stagnation_pressure
    high_pressure_turbine.inputs.fuel_to_air_ratio        = combustor.outputs.fuel_to_air_ratio 
    high_pressure_turbine.inputs.compressor               = compressor.outputs 
    high_pressure_turbine.inputs.bypass_ratio             = 0.0
    high_pressure_turbine.inputs.fan                      = Data()
    high_pressure_turbine.inputs.fan.work_done            = 0.0
    compute_turbine_performance(high_pressure_turbine,conditions)
            
    #link the low pressure turbine to the high pressure turbine
    low_pressure_turbine.inputs.stagnation_temperature    = high_pressure_turbine.outputs.stagnation_temperature
    low_pressure_turbine.inputs.stagnation_pressure       = high_pressure_turbine.outputs.stagnation_pressure
    
    #link the low pressure turbine to the low_pressure_compresor
    low_pressure_turbine.inputs.compressor                 = Data()
    low_pressure_turbine.inputs.compressor.work_done       = 0.0
    
    #link the low pressure turbine to the combustor
    low_pressure_turbine.inputs.fuel_to_air_ratio         = combustor.outputs.fuel_to_air_ratio
    
    #flow through the low pressure turbine
    low_pressure_turbine.inputs.bypass_ratio              = 0.0
    low_pressure_turbine.inputs.fan                       = Data()
    low_pressure_turbine.inputs.fan.work_done             = 0.0
    compute_turbine_performance(low_pressure_turbine,conditions)
    
    #link the core nozzle to the low pressure turbine
    core_nozzle.inputs.stagnation_temperature             = low_pressure_turbine.outputs.stagnation_temperature
    core_nozzle.inputs.stagnation_pressure                = low_pressure_turbine.outputs.stagnation_pressure
    
    #flow through the core nozzle
    compute_expansion_nozzle_performance(core_nozzle,conditions)

    # compute the thrust using the thrust component
    #link the thrust component to the core nozzle
    turboshaft.inputs.core_exit_velocity                  = core_nozzle.outputs.velocity
    turboshaft.inputs.core_area_ratio                     = core_nozzle.outputs.area_ratio
    turboshaft.inputs.core_nozzle                         = core_nozzle.outputs
    
    #link the thrust component to the combustor
    turboshaft.inputs.fuel_to_air_ratio                   = combustor.outputs.fuel_to_air_ratio
    
    #link the thrust component to the low pressure compressor 
    turboshaft.inputs.stag_temp_lpt_exit                  = compressor.inputs.stagnation_temperature
    turboshaft.inputs.stag_press_lpt_exit                 = compressor.inputs.stagnation_pressure 
    turboshaft.inputs.total_temperature_reference         = compressor.inputs.stagnation_temperature
    turboshaft.inputs.total_pressure_reference            = compressor.inputs.stagnation_pressure  

    #compute the power
    turboshaft.inputs.fan_nozzle                          = Data()
    turboshaft.inputs.fan_nozzle.velocity                 = 0.0
    turboshaft.inputs.fan_nozzle.area_ratio               = 0.0
    turboshaft.inputs.fan_nozzle.static_pressure          = 0.0
    turboshaft.inputs.bypass_ratio                        = 0.0
    turboshaft.inputs.flow_through_core                   = 1.0 #scaled constant to turn on core power computation
    turboshaft.inputs.flow_through_fan                    = 0.0 #scaled constant to turn on fan power computation      
    
    # compute the powert
    size_core(turboshaft,conditions) 
    
    # Static Sea Level Thrust  
    atmosphere_sls                                        = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmo_data                                             = atmosphere_sls.compute_values(0.0,0.0)
    
    p                                                     = atmo_data.pressure          
    T                                                     = atmo_data.temperature       
    rho                                                   = atmo_data.density          
    a                                                     = atmo_data.speed_of_sound    
    mu                                                    = atmo_data.dynamic_viscosity      

    # setup conditions
    conditions_sls = RCAIDE.Framework.Mission.Common.Results()

    # freestream conditions    
    conditions_sls.freestream.altitude                    = np.atleast_1d(0)
    conditions_sls.freestream.mach_number                 = np.atleast_1d(0.01)
    conditions_sls.freestream.pressure                    = np.atleast_1d(p)
    conditions_sls.freestream.temperature                 = np.atleast_1d(T)
    conditions_sls.freestream.density                     = np.atleast_1d(rho)
    conditions_sls.freestream.dynamic_viscosity           = np.atleast_1d(mu)
    conditions_sls.freestream.gravity                     = np.atleast_2d(planet.sea_level_gravity)
    conditions_sls.freestream.isentropic_expansion_factor = np.atleast_1d(turboshaft.working_fluid.compute_gamma(T,p))
    conditions_sls.freestream.Cp                          = np.atleast_1d(turboshaft.working_fluid.compute_cp(T,p))
    conditions_sls.freestream.R                           = np.atleast_1d(turboshaft.working_fluid.gas_specific_constant)
    conditions_sls.freestream.speed_of_sound              = np.atleast_1d(a)
    conditions_sls.freestream.velocity                    = np.atleast_1d(a*0.01)   
     
    compute_power(turboshaft,conditions_sls,throttle = 1.0) 
    turboshaft.sealevel_static_power = turboshaft.outputs.power
        
    return      
  