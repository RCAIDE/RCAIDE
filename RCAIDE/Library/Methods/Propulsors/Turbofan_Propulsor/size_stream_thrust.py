# RCAIDE/Library/Methods/Propulsors/Turbofan_Propulsor/compute_thrust.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from RCAIDE.Library.Methods.Propulsors.Turbofan_Propulsor            import compute_stream_thrust

# Python package imports
import RNUMPY as rp

# ----------------------------------------------------------------------------------------------------------------------
#   size_stream_thrust
# ----------------------------------------------------------------------------------------------------------------------
def size_stream_thrust(turbofan,turbofan_conditions,freestream): 
    """Sizes the core flow for the design condition. 

       Assumptions: 
           Working fluid is a perfect gas

       Source: 
           Heiser, William H., Pratt, D. T., Daley, D. H., and Unmeel, B. M., 
           "Hypersonic Airbreathing Propulsors", 1994 
           Chapter 4 - pgs. 175-180
           
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
    
    # Unpack Flight conditions
    a0                            = freestream.speed_of_sound 
    turbofan_conditions.throttle  = 1.0 
    
    # Unpack properties from turbofan 
    Tref   = turbofan.reference_temperature 
    Pref   = turbofan.reference_pressure   
    Tt_ref = turbofan_conditions.total_temperature_reference  
    Pt_ref = turbofan_conditions.total_pressure_reference  
    
    #compute nondimensional thrust 
    compute_stream_thrust(turbofan, turbofan_conditions, freestream)
    
    #compute dimensional mass flow rates 
    Fsp                         = turbofan_conditions.non_dimensional_thrust 
    mdot_core                   = turbofan.design_thrust/(Fsp*a0*turbofan_conditions.throttle)   
    mdhc                        = mdot_core/ (rp.sqrt(Tref/Tt_ref)*(Pt_ref/Pref)) 
    
    # Store results on turbofan data structure 
    turbofan.mass_flow_rate_design               = mdot_core 
    turbofan.compressor_nondimensional_massflow  = mdhc 
    
    return        
