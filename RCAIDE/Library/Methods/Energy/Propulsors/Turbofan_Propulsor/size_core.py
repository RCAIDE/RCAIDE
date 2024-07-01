## @ingroup Library-Methods-Energy-Propulsors-Turbofan_Propulsor
# RCAIDE/Library/Methods/Energy/Propulsors/Turbofan_Propulsor/size_core.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from RCAIDE.Library.Methods.Energy.Propulsors.Turbofan_Propulsor            import compute_thrust

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  size_core
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Energy-Propulsors-Turbofan_Propulsor 
def size_core(turbofan,conditions):
    """Sizes the core flow for the design condition by computing the
    non-dimensional thrust 

    Assumptions:
        Working fluid is a perfect gas

    Source:
        https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Args:
        conditions.freestream.speed_of_sound  (numpy.ndarray): [m/s]  
        turbofan
          .inputs.bypass_ratio                (float): bypass_ratio                [-]
          .inputs.total_temperature_reference (float): total temperature reference [K]
          .inputs.total_pressure_reference    (float): total pressure reference    [Pa]  
          .reference_temperature              (float): reference temperature       [K]
          .reference_pressure                 (float): reference pressure          [Pa]
          .design_thrust                      (float): design thrust               [N]  

    Returns:
        None 
    """             
    # Unpack flight conditions 
    a0             = conditions.freestream.speed_of_sound

    # Unpack turbofan flight conditions 
    bypass_ratio   = turbofan.inputs.bypass_ratio
    Tref           = turbofan.reference_temperature
    Pref           = turbofan.reference_pressure 
    throttle       = 1.0 
    Tt_ref         = turbofan.inputs.total_temperature_reference  
    Pt_ref         = turbofan.inputs.total_pressure_reference 

    # Compute nondimensional thrust
    compute_thrust(turbofan,conditions) 

    # Compute dimensional mass flow rates
    Fsp        = turbofan.outputs.non_dimensional_thrust
    mdot_core  = turbofan.design_thrust/(Fsp*a0*(1+bypass_ratio)*throttle)  
    mdhc       = mdot_core/ (np.sqrt(Tref/Tt_ref)*(Pt_ref/Pref))

    # Store results on turbofan data structure 
    turbofan.mass_flow_rate_design               = mdot_core
    turbofan.compressor_nondimensional_massflow  = mdhc

    return  
