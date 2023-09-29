## @ingroup Methods-Propulsion
# ducted_fan_sizing.py
# 
# Created:  Michael Vegh, July 2015
# Modified: 
#        

""" create and evaluate a Ducted Fan network
"""

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
import RCAIDE
import numpy as np
from RCAIDE.Core import Data

## @ingroup Methods-Propulsion
def design_ducted_fan(ducted_fan):  
    """
    creates and evaluates a ducted_fan network based on an atmospheric sizing condition
    
    Inputs:
    ducted_fan       ducted fan network object (to be modified)
    mach_number
    altitude         [meters]
    delta_isa        temperature difference [K]
    conditions       ordered dict object
    """
      
    if(ducted_fan.design_mach_number==None or ducted_fan.design_altitude==None): 
        raise NameError('The sizing conditions require an altitude and a Mach number') 
    else:
        #call the atmospheric model to get the conditions at the specified altitude
        atmosphere = RCAIDE.Analyses.Atmospheric.US_Standard_1976()
        atmo_data = atmosphere.compute_values(ducted_fan.design_altitude,ducted_fan.design_isa_deviation)
        planet    = RCAIDE.Attributes.Planets.Earth()
        
        p   = atmo_data.pressure          
        T   = atmo_data.temperature       
        rho = atmo_data.density          
        a   = atmo_data.speed_of_sound    
        mu  = atmo_data.dynamic_viscosity   
    
        # setup conditions
        conditions = RCAIDE.Analyses.Mission.Common.Results()           

        # freestream conditions           
        conditions.freestream.altitude                    = np.atleast_1d(ducted_fan.design_altitude)
        conditions.freestream.mach_number                 = np.atleast_1d(ducted_fan.design_mach_number)
        conditions.freestream.pressure                    = np.atleast_1d(p)
        conditions.freestream.temperature                 = np.atleast_1d(T)
        conditions.freestream.density                     = np.atleast_1d(rho)
        conditions.freestream.dynamic_viscosity           = np.atleast_1d(mu)
        conditions.freestream.gravity                     = np.atleast_1d(planet.compute_gravity(ducted_fan.design_altitude)                                                                                                    )
        conditions.freestream.isentropic_expansion_factor = np.atleast_1d(ducted_fan.working_fluid.compute_gamma(T,p))
        conditions.freestream.Cp                          = np.atleast_1d(ducted_fan.working_fluid.compute_cp(T,p))
        conditions.freestream.R                           = np.atleast_1d(ducted_fan.working_fluid.gas_specific_constant)
        conditions.freestream.speed_of_sound              = np.atleast_1d(a)
        conditions.freestream.velocity                    = conditions.freestream.mach_number*conditions.freestream.speed_of_sound 
    
    # Setup Components   
    ram                       = ducted_fan.ram
    inlet_nozzle              = ducted_fan.inlet_nozzle
    fan                       = ducted_fan.fan
    fan_nozzle                = ducted_fan.fan_nozzle  
    bypass_ratio              = ducted_fan.bypass_ratio  
    
    #set the working fluid to determine the fluid properties
    ram.inputs.working_fluid = ducted_fan.working_fluid
    
    #Flow through the ram , this computes the necessary flow quantities and stores it into conditions
    ram(conditions)

    #link inlet nozzle to ram 
    inlet_nozzle.inputs = ram.outputs
    
    #Flow through the inlet nozzle
    inlet_nozzle(conditions)
        
    #Link the fan to the inlet nozzle
    fan.inputs = inlet_nozzle.outputs
    
    #flow through the fan
    fan(conditions)        
    
    #link the dan nozzle to the fan
    fan_nozzle.inputs =  fan.outputs
    
    # flow through the fan nozzle
    fan_nozzle(conditions)
    
    # compute the thrust using the thrust component
    
    #link the thrust component to the fan nozzle
    ducted_fan.inputs.fan_exit_velocity                        = fan_nozzle.outputs.velocity
    ducted_fan.inputs.fan_area_ratio                           = fan_nozzle.outputs.area_ratio
    ducted_fan.inputs.fan_nozzle                               = fan_nozzle.outputs 
    ducted_fan.inputs.bypass_ratio                             = bypass_ratio
    ducted_fan.inputs.total_temperature_reference              = fan_nozzle.outputs.stagnation_temperature
    ducted_fan.inputs.total_pressure_reference                 = fan_nozzle.outputs.stagnation_pressure
    ducted_fan.inputs.flow_through_core                        = 0.
    ducted_fan.inputs.flow_through_fan                         = 1.
    
    #nonexistant components used to run thrust
    ducted_fan.inputs.core_exit_velocity                       = 0.
    ducted_fan.inputs.core_area_ratio                          = 0.
    ducted_fan.inputs.core_nozzle                              = Data()
    ducted_fan.inputs.core_nozzle.velocity                     = 0.
    ducted_fan.inputs.core_nozzle.area_ratio                   = 0.
    ducted_fan.inputs.core_nozzle.static_pressure              = 0.                                                                                                                
    
    #compute the trust
    ducted_fan.size_fan(conditions)
    
    return ducted_fan
       
    