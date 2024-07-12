## @ingroup Methods-Energy-Propulsors-Turbofan_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Turbofan_Propulsor/design_turbofan.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE Imports
import RCAIDE
from RCAIDE.Library.Methods.Propulsors.Converters.Ram                import compute_ram_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Combustor          import compute_combustor_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Compressor         import compute_compressor_performance 
from RCAIDE.Library.Methods.Propulsors.Converters.Fan                import compute_fan_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Turbine            import compute_turbine_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Expansion_Nozzle   import compute_expansion_nozzle_performance 
from RCAIDE.Library.Methods.Propulsors.Converters.Compression_Nozzle import compute_compression_nozzle_performance
from RCAIDE.Library.Methods.Propulsors.Turbofan_Propulsor            import size_core , compute_performance

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Design Turbofan
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Energy-Propulsors-Turbofan_Propulsor
def design_turbofan(turbofan):
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
    
    #Creating the network by manually linking the different components
    
    #set the working fluid to determine the fluid properties
    ram.inputs.working_fluid                             = turbofan.working_fluid
    
    # Flow through the ram , this computes the necessary flow quantities and stores it into conditions
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
    
    # flow through the fan
    compute_fan_performance(fan,conditions)
    
    #link the combustor to the high pressure compressor
    combustor.inputs.stagnation_temperature                = high_pressure_compressor.outputs.stagnation_temperature
    combustor.inputs.stagnation_pressure                   = high_pressure_compressor.outputs.stagnation_pressure
    
    #flow through the high pressor comprresor
    compute_combustor_performance(combustor,conditions)
    
    #link the high pressure turbione to the combustor
    high_pressure_turbine.inputs.stagnation_temperature    = combustor.outputs.stagnation_temperature
    high_pressure_turbine.inputs.stagnation_pressure       = combustor.outputs.stagnation_pressure
    high_pressure_turbine.inputs.fuel_to_air_ratio         = combustor.outputs.fuel_to_air_ratio
    
    #link the high pressure turbine to the high pressure compressor
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
    low_pressure_turbine.inputs.fan                        =  fan.outputs
    
    #get the bypass ratio from the thrust component
    low_pressure_turbine.inputs.bypass_ratio               =  bypass_ratio
    
    #flow through the low pressure turbine
    compute_turbine_performance(low_pressure_turbine,conditions)
    
    #link the core nozzle to the low pressure turbine
    core_nozzle.inputs.stagnation_temperature              = low_pressure_turbine.outputs.stagnation_temperature
    core_nozzle.inputs.stagnation_pressure                 = low_pressure_turbine.outputs.stagnation_pressure
    
    #flow through the core nozzle
    compute_expansion_nozzle_performance(core_nozzle,conditions)
   
    #link the fan nozzle to the fan
    fan_nozzle.inputs.stagnation_temperature               = fan.outputs.stagnation_temperature
    fan_nozzle.inputs.stagnation_pressure                  = fan.outputs.stagnation_pressure
    
    #flow through the fan nozzle
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
    turbofan.inputs.flow_through_core                        =  1./(1.+bypass_ratio) #scaled constant to turn on core thrust computation
    turbofan.inputs.flow_through_fan                         =  bypass_ratio/(1.+bypass_ratio) #scaled constant to turn on fan thrust computation     

    #compute the thrust
    size_core(turbofan,conditions)
    
    
    # Static Sea Level Thrust  
    atmosphere_sls = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmo_data = atmosphere_sls.compute_values(0.0,0.0)
    
    p   = atmo_data.pressure          
    T   = atmo_data.temperature       
    rho = atmo_data.density          
    a   = atmo_data.speed_of_sound    
    mu  = atmo_data.dynamic_viscosity      
    # setup conditions 
    fuel_line                               = RCAIDE.Library.Components.Energy.Distribution.Fuel_Line()    
    fuel_tank                               = RCAIDE.Library.Components.Energy.Fuel_Tanks.Fuel_Tank()  
    fuel                                    = RCAIDE.Library.Attributes.Propellants.Aviation_Gasoline()    
    fuel_tank.fuel                          = fuel  
    fuel_line.fuel_tanks.append(fuel_tank)  
    fuel_line.propulsors.append(turbofan)  
        
    sls_conditions = RCAIDE.Framework.Mission.Common.Results()

    # freestream conditions    
    sls_conditions.freestream.altitude                    = np.atleast_1d(0)
    sls_conditions.freestream.mach_number                 = np.atleast_1d(0.01)
    sls_conditions.freestream.pressure                    = np.atleast_1d(p)
    sls_conditions.freestream.temperature                 = np.atleast_1d(T)
    sls_conditions.freestream.density                     = np.atleast_1d(rho)
    sls_conditions.freestream.dynamic_viscosity           = np.atleast_1d(mu)
    sls_conditions.freestream.gravity                     = np.atleast_2d(planet.sea_level_gravity)
    sls_conditions.freestream.isentropic_expansion_factor = np.atleast_1d(turbofan.working_fluid.compute_gamma(T,p))
    sls_conditions.freestream.Cp                          = np.atleast_1d(turbofan.working_fluid.compute_cp(T,p))
    sls_conditions.freestream.R                           = np.atleast_1d(turbofan.working_fluid.gas_specific_constant)
    sls_conditions.freestream.speed_of_sound              = np.atleast_1d(a)
    sls_conditions.freestream.velocity                    = np.atleast_1d(a*0.01)   

    # initialize data structure for turbofan operating conditions (for energy ) 
    sls_conditions.energy[fuel_line.tag]                                  = RCAIDE.Framework.Mission.Common.Conditions()  
    sls_conditions.energy[fuel_line.tag][fuel_tank.tag]                   = RCAIDE.Framework.Mission.Common.Conditions()  
    sls_conditions.energy[fuel_line.tag][fuel_tank.tag].mass_flow_rate    = np.zeros((1,1))     
    sls_conditions.energy[fuel_line.tag][fuel_tank.tag].mass              = np.zeros((1,1))   
    sls_conditions.energy[fuel_line.tag][turbofan.tag]                    = RCAIDE.Framework.Mission.Common.Conditions() 
    sls_conditions.energy[fuel_line.tag][turbofan.tag].throttle           = np.array([[1.0]])
    sls_conditions.energy[fuel_line.tag][turbofan.tag].y_axis_rotation    = np.zeros((1,1)) 
    sls_conditions.energy[fuel_line.tag][turbofan.tag].thrust             = np.zeros((1,1))
    sls_conditions.energy[fuel_line.tag][turbofan.tag].power              = np.zeros((1,1))
    

    # initialize data structure for turbofan operating conditions (for noise )       
    sls_conditions.noise[fuel_line.tag]                                 = RCAIDE.Framework.Mission.Common.Conditions()              
    sls_conditions.noise[fuel_line.tag][turbofan.tag]                   = RCAIDE.Framework.Mission.Common.Conditions() 
    sls_conditions.noise[fuel_line.tag][turbofan.tag].turbofan          = RCAIDE.Framework.Mission.Common.Conditions()
    
    total_power     = np.zeros((3,1))
    total_thrust    = np.zeros((1,1))
    compute_performance(sls_conditions,fuel_line,turbofan,total_thrust,total_power) 
    turbofan.sealevel_static_thrust = turbofan.outputs.thrust
    
    
    return 