## @ingroup Methods-Energy-Propulsors-Turbojet_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Turbojet_Propulsor/size_core.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from RCAIDE.Methods.Energy.Propulsors.Turbojet_Propulsor import compute_thrust

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  size_core
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Energy-Propulsors-Turbojet_Propulsor 
def size_core(turbojet,conditions):
    """Sizes the core flow for the design condition.

    Assumptions:
    Perfect gas

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Inputs:
    conditions.freestream.speed_of_sound [m/s] (conditions is also passed to turbojet.compute(..))
    turbojet.inputs.
      bypass_ratio                       [-]
      total_temperature_reference        [K]
      total_pressure_reference           [Pa]
      number_of_engines                  [-]

    Outputs:
    turbojet.outputs.non_dimensional_thrust  [-]

    Properties Used:
    turbojet.
      reference_temperature              [K]
      reference_pressure                 [Pa]
      total_design                       [N] - Design thrust
    """             
    #unpack inputs
    a0                   = conditions.freestream.speed_of_sound
    throttle             = 1.0

    #unpack from turbojet
    bypass_ratio                = turbojet.inputs.bypass_ratio
    Tref                        = turbojet.reference_temperature
    Pref                        = turbojet.reference_pressure 

    total_temperature_reference = turbojet.inputs.total_temperature_reference  # low pressure turbine output for turbofan
    total_pressure_reference    = turbojet.inputs.total_pressure_reference 

    #compute nondimensional thrust
    compute_thrust(turbojet,conditions)

    #unpack results 
    Fsp                         = turbojet.outputs.non_dimensional_thrust

    #compute dimensional mass flow rates
    mdot_core                   = turbojet.design_thrust/(Fsp*a0*(1+bypass_ratio)*throttle)  
    mdhc                        = mdot_core/ (np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref))

    #pack outputs
    turbojet.mass_flow_rate_design               = mdot_core
    turbojet.compressor_nondimensional_massflow  = mdhc

    return    
