## @ingroup Library-Methods-Energy-Propulsors-Turboshaft_Propulsor
# RCAIDE/Library/Methods/Energy/Propulsors/Turboshaft_Propulsor/design_turboshaft.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

# RCAIDE Imports     
import RCAIDE
from RCAIDE.Framework.Core                                           import Data
from RCAIDE.Framework.Mission.Common                                 import Conditions
from RCAIDE.Library.Methods.Propulsors.Converters.Ram                import compute_ram_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Combustor          import compute_combustor_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Compressor         import compute_compressor_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Turbine            import compute_turbine_performance
from RCAIDE.Library.Methods.Propulsors.Converters.Expansion_Nozzle   import compute_expansion_nozzle_performance 
from RCAIDE.Library.Methods.Propulsors.Converters.Compression_Nozzle import compute_compression_nozzle_performance
from RCAIDE.Library.Methods.Propulsors.Turboshaft_Propulsor          import size_core 
from RCAIDE.Library.Methods.Propulsors.Common                        import compute_static_sea_level_performance 

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
         
         
    fuel_line                = RCAIDE.Library.Components.Energy.Distributors.Fuel_Line()
    segment                  = RCAIDE.Framework.Mission.Segments.Segment()  
    segment.state.conditions = conditions
    segment.state.conditions.energy[fuel_line.tag] = Conditions()
    segment.state.conditions.noise[fuel_line.tag] = Conditions()
    turboshaft.append_operating_conditions(segment,fuel_line) 
    for tag, item in  turboshaft.items(): 
        if issubclass(type(item), RCAIDE.Library.Components.Component):
            item.append_operating_conditions(segment,fuel_line,turboshaft) 
         
    ram                                                   = turboshaft.ram
    inlet_nozzle                                          = turboshaft.inlet_nozzle
    compressor                                            = turboshaft.compressor
    combustor                                             = turboshaft.combustor
    high_pressure_turbine                                 = turboshaft.high_pressure_turbine
    low_pressure_turbine                                  = turboshaft.low_pressure_turbine
    core_nozzle                                           = turboshaft.core_nozzle  

    # unpack component conditions
    turboshaft_conditions   = conditions.energy[fuel_line.tag][turboshaft.tag]
    ram_conditions          = turboshaft_conditions[ram.tag]     
    inlet_nozzle_conditions = turboshaft_conditions[inlet_nozzle.tag]
    core_nozzle_conditions  = turboshaft_conditions[core_nozzle.tag] 
    compressor_conditions   = turboshaft_conditions[compressor.tag]  
    combustor_conditions    = turboshaft_conditions[combustor.tag]
    lpt_conditions          = turboshaft_conditions[low_pressure_turbine.tag]
    hpt_conditions          = turboshaft_conditions[high_pressure_turbine.tag] 
     
    # Step 1: Set the working fluid to determine the fluid properties
    ram.working_fluid                             = turboshaft.working_fluid

    # Step 2: Compute flow through the ram , this computes the necessary flow quantities and stores it into conditions
    compute_ram_performance(ram,ram_conditions,conditions)

    # Step 3: link inlet nozzle to ram 
    inlet_nozzle_conditions.inputs.stagnation_temperature             = ram_conditions.outputs.stagnation_temperature
    inlet_nozzle_conditions.inputs.stagnation_pressure                = ram_conditions.outputs.stagnation_pressure

    # Step 4: Compute flow through the inlet nozzle
    compute_compression_nozzle_performance(inlet_nozzle,inlet_nozzle_conditions,conditions)      

    # Step 5: Link low pressure compressor to the inlet nozzle
    compressor_conditions.inputs.stagnation_temperature  = inlet_nozzle_conditions.outputs.stagnation_temperature
    compressor_conditions.inputs.stagnation_pressure     = inlet_nozzle_conditions.outputs.stagnation_pressure

    # Step 6: Compute flow through the low pressure compressor
    compute_compressor_performance(compressor,compressor_conditions,conditions)
    
    # Step 11: Link the combustor to the high pressure compressor
    combustor_conditions.inputs.stagnation_temperature                = compressor_conditions.outputs.stagnation_temperature
    combustor_conditions.inputs.stagnation_pressure                   = compressor_conditions.outputs.stagnation_pressure
    
    # Step 12: Compute flow through the high pressor comprresor
    compute_combustor_performance(combustor,combustor_conditions,conditions) 

    #link the high pressure turbione to the combustor
    hpt_conditions.inputs.stagnation_temperature   = combustor_conditions.outputs.stagnation_temperature
    hpt_conditions.inputs.stagnation_pressure      = combustor_conditions.outputs.stagnation_pressure
    hpt_conditions.inputs.fuel_to_air_ratio        = combustor_conditions.outputs.fuel_to_air_ratio 
    hpt_conditions.inputs.compressor               = compressor_conditions.outputs 
    hpt_conditions.inputs.bypass_ratio             = 0.0
    hpt_conditions.inputs.fan                      = Data()
    hpt_conditions.inputs.fan.work_done            = 0.0
    compute_turbine_performance(high_pressure_turbine,hpt_conditions,conditions)
            
    #link the low pressure turbine to the high pressure turbine
    lpt_conditions.inputs.stagnation_temperature    = hpt_conditions.outputs.stagnation_temperature
    lpt_conditions.inputs.stagnation_pressure       = hpt_conditions.outputs.stagnation_pressure
    
    #link the low pressure turbine to the low_pressure_compresor
    lpt_conditions.inputs.compressor                = Data()
    lpt_conditions.inputs.compressor.work_done      = 0.0
    
    #link the low pressure turbine to the combustor
    lpt_conditions.inputs.fuel_to_air_ratio         = combustor_conditions.outputs.fuel_to_air_ratio
    
    #flow through the low pressure turbine
    lpt_conditions.inputs.bypass_ratio              = 0.0
    lpt_conditions.inputs.fan                       = Data()
    lpt_conditions.inputs.fan.work_done             = 0.0
    compute_turbine_performance(low_pressure_turbine,lpt_conditions,conditions)
    
    #link the core nozzle to the low pressure turbine
    core_nozzle_conditions.inputs.stagnation_temperature             = lpt_conditions.outputs.stagnation_temperature
    core_nozzle_conditions.inputs.stagnation_pressure                = lpt_conditions.outputs.stagnation_pressure
    
    #flow through the core nozzle
    compute_expansion_nozzle_performance(core_nozzle,core_nozzle_conditions,conditions)

    # compute the thrust using the thrust component
    #link the thrust component to the core nozzle
    turboshaft_conditions.core_exit_velocity                  = core_nozzle_conditions.outputs.velocity
    turboshaft_conditions.core_area_ratio                     = core_nozzle_conditions.outputs.area_ratio
    turboshaft_conditions.core_nozzle                         = core_nozzle_conditions.outputs
    
    #link the thrust component to the combustor
    turboshaft_conditions.fuel_to_air_ratio                   = combustor_conditions.outputs.fuel_to_air_ratio
    
    #link the thrust component to the low pressure compressor
    turboshaft_conditions.combustor_stagnation_temperature    = combustor_conditions.outputs.stagnation_temperature
    turboshaft_conditions.stag_temp_lpt_exit                  = compressor_conditions.inputs.stagnation_temperature
    turboshaft_conditions.stag_press_lpt_exit                 = compressor_conditions.inputs.stagnation_pressure 
    turboshaft_conditions.total_temperature_reference         = compressor_conditions.inputs.stagnation_temperature
    turboshaft_conditions.total_pressure_reference            = compressor_conditions.inputs.stagnation_pressure  

    #compute the power
    turboshaft_conditions.fan_nozzle                          = Data()
    turboshaft_conditions.fan_nozzle.velocity                 = 0.0
    turboshaft_conditions.fan_nozzle.area_ratio               = 0.0
    turboshaft_conditions.fan_nozzle.static_pressure          = 0.0
    turboshaft_conditions.bypass_ratio                        = 0.0
    turboshaft_conditions.flow_through_core                   = 1.0 #scaled constant to turn on core power computation
    turboshaft_conditions.flow_through_fan                    = 0.0 #scaled constant to turn on fan power computation      
    
    # Step 25: Size the core of the turboshaft  
    size_core(turboshaft,turboshaft_conditions,conditions)
    
    # Step 26: Static Sea Level Thrust 
    compute_static_sea_level_performance(turboshaft)
     
    return      
  