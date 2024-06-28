## @ingroup Methods-Energy-Propulsors-Converters-Engine
# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Engine/compute_power_from_throttle.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
 # RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Core import Units

# package imports
import numpy as np 

# ---------------------------------------------------------------------------------------------------------------------- 
# compute_power_from_throttle
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Energy-Propulsors-Converters-Engine
def compute_power_from_throttle(engine,conditions,throttle):
    """ The internal combustion engine output power and specific power consumption.
    The following properties are computed:
    engine
      .outputs.power                           (numpy.ndarray): Brake power (or Shaft power)              [W]
      .outputs.power_specific_fuel_consumption (numpy.ndarray): Power (brake) specific fuel consumption   [lbf/(HP· h) 
      .outputs.fuel_flow_rate                  (numpy.ndarray): Fuel flow                                 [kg/s]
      .outputs.torque                          (numpy.ndarray): Torque                                    [Q]
    
    Source:
        Gagg and Ferrar model (ref: S. Gudmundsson, 2014 - eq. 7-16)
    
    Assumtions:
        Available power based on Gagg and Ferrar model (ref: S. Gudmundsson, 2014 - eq. 7-16)
    
    Args:
        engine
          .sea_level_power                        (float): sea-level power      [W]
          .flat_rate_altitude                     (float): flat rate altitude   [meters]
          .power_specific_fuel_consumption        (float): PSFC                 [RPM]
          .throttle setting               (numpy.ndarray): throttle             [unitless]
          .inputs.speed                   (numpy.ndarray): angular velocity     [rad/s]
        freestream conditions 
          .altitude                               (float): altitde              [meters]
          .delta_isa                              (float): altitude offset      [meters]
            
    Returns:
        None 
    """

    # Unpack
    altitude    = conditions.freestream.altitude
    delta_isa   = conditions.freestream.delta_ISA 
    PSLS        = engine.sea_level_power
    h_flat      = engine.flat_rate_altitude
    omega       = engine.inputs.speed
    PSFC        = engine.power_specific_fuel_consumption

    # shift in power lapse due to flat rate
    altitude_virtual = altitude - h_flat       
    altitude_virtual[altitude_virtual<0.] = 0. 

    # Compute the sea-level ISA atmosphere conditions
    atmo             = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmo_values_0    = atmo.compute_values(0,0) 
    rho0             = atmo_values_0.density[0,0]     
    atmo_values      = atmo.compute_values(altitude_virtual,delta_isa) 
    rho              = atmo_values.density 
    
    # Compute the density ratio:
    sigma = rho / rho0
    
    # Compute available power 
    Pavailable                    = PSLS * (sigma - 0.117) / 0.883        
    Pavailable[h_flat > altitude] = PSLS

    # Regulate using throttle 
    output_power                  = Pavailable * throttle 
    output_power[output_power<0.] = 0. 
    SFC                           = PSFC * Units['lb/hp/hr']

    # Compute engine torque
    torque = output_power/omega
    
    # Determine fuel flow rate
    alt_0           = np.zeros_like(altitude)
    fuel_flow_rate  = np.fmax(output_power*SFC,alt_0) 
    
    # Store results 
    engine.outputs.power                           = output_power
    engine.outputs.power_specific_fuel_consumption = PSFC
    engine.outputs.fuel_flow_rate                  = fuel_flow_rate
    engine.outputs.torque                          = torque

    return
