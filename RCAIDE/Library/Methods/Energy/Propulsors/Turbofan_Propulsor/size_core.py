## @ingroup Methods-Energy-Propulsors-Turbofan_Propulsor
# RCAIDE/Library/Methods/Energy/Propulsors/Turbofan_Propulsor/size_core.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from RCAIDE.Library.Methods.Energy.Propulsors.Turbofan_Propulsor            import compute_thrust

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  size_core
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Energy-Propulsors-Turbofan_Propulsor 
def size_core(turbofan,conditions):
    """Sizes the core flow for the design condition.

    Assumptions:
    Perfect gas

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Inputs:
    conditions.freestream.speed_of_sound [m/s]  
    turbofan.inputs.
      bypass_ratio                       [-]
      total_temperature_reference        [K]
      total_pressure_reference           [Pa]
      number_of_engines                  [-]

    Outputs:
    turbofan.outputs.non_dimensional_thrust  [-]

    Properties Used:
    turbofan.
      reference_temperature              [K]
      reference_pressure                 [Pa]
      total_design                       [N] - Design thrust
    """             
    #unpack inputs
    a0                   = conditions.freestream.speed_of_sound
    throttle             = 1.0

    #unpack from turbofan
    bypass_ratio                = turbofan.inputs.bypass_ratio
    Tref                        = turbofan.reference_temperature
    Pref                        = turbofan.reference_pressure 

    total_temperature_reference = turbofan.inputs.total_temperature_reference  # low pressure turbine output for turbofan
    total_pressure_reference    = turbofan.inputs.total_pressure_reference 

    #compute nondimensional thrust
    compute_thrust(turbofan,conditions)

    #unpack results 
    Fsp                         = turbofan.outputs.non_dimensional_thrust

    #compute dimensional mass flow rates
    mdot_core                   = turbofan.design_thrust/(Fsp*a0*(1+bypass_ratio)*throttle)  
    mdhc                        = mdot_core/ (np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref))

    #pack outputs
    turbofan.mass_flow_rate_design               = mdot_core
    turbofan.compressor_nondimensional_massflow  = mdhc

    return  
