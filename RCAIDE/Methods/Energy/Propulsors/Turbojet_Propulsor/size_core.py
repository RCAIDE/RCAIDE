## @ingroup Methods-Energy-Propulsors-Turbojet_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Turbojet_Propulsor/size_core.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  size_core
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Energy-Propulsors-Turbojet_Propulsor 
def size_core(self,conditions):
    """Sizes the core flow for the design condition.

    Assumptions:
    Perfect gas

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Inputs:
    conditions.freestream.speed_of_sound [m/s] (conditions is also passed to self.compute(..))
    self.inputs.
      bypass_ratio                       [-]
      total_temperature_reference        [K]
      total_pressure_reference           [Pa]
      number_of_engines                  [-]

    Outputs:
    self.outputs.non_dimensional_thrust  [-]

    Properties Used:
    self.
      reference_temperature              [K]
      reference_pressure                 [Pa]
      total_design                       [N] - Design thrust
    """             
    #unpack inputs
    a0                   = conditions.freestream.speed_of_sound
    throttle             = 1.0

    #unpack from self
    bypass_ratio                = self.inputs.bypass_ratio
    Tref                        = self.reference_temperature
    Pref                        = self.reference_pressure 

    total_temperature_reference = self.inputs.total_temperature_reference  # low pressure turbine output for turbofan
    total_pressure_reference    = self.inputs.total_pressure_reference 

    #compute nondimensional thrust
    self.compute_thrust(conditions)

    #unpack results 
    Fsp                         = self.outputs.non_dimensional_thrust

    #compute dimensional mass flow rates
    mdot_core                   = self.design_thrust/(Fsp*a0*(1+bypass_ratio)*throttle)  
    mdhc                        = mdot_core/ (np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref))

    #pack outputs
    self.mass_flow_rate_design               = mdot_core
    self.compressor_nondimensional_massflow  = mdhc

    return    
