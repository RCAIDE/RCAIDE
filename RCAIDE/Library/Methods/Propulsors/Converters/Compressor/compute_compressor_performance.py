# RCAIDE/Library/Methods/Propulsors/Converters/Compressor/compute_compressor_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ---------------------------------------------------------------------------------------------------------------------- 
# compute_compression_nozzle_performance
# ----------------------------------------------------------------------------------------------------------------------  
def compute_compressor_performance(compressor,compressor_conditions,freestream):
    """ Computes the performance of a compressor bases on its polytropic efficiency.
        The following properties are computed: 
       compressor.outputs.
         stagnation_temperature  (numpy.ndarray): exit stagnation_temperature   [K]  
         stagnation_pressure     (numpy.ndarray): exit stagnation_pressure      [Pa]
         stagnation_enthalpy     (numpy.ndarray): exit stagnation_enthalpy      [J/kg]
         work_done               (numpy.ndarray): work done                     [J/kg] 

    Assumptions:
        Constant polytropic efficiency and pressure ratio

    Source:
        https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Args:
        conditions.freestream.
          isentropic_expansion_factor         (numpy.ndarray): isentropic_expansion_factor        [unitless]
          specific_heat_at_constant_pressure  (numpy.ndarray): specific_heat_at_constant_pressure [J/(kg K)]
        compressor.
           inputs.stagnation_temperature      (numpy.ndarray): entering stagnation temperature [K]
           inputs.stagnation_pressure         (numpy.ndarray): entering stagnation pressure    [Pa] 
           pressure_ratio                             (float): pressure ratio                  [unitless]
           polytropic_efficiency                      (float): polytropic efficiency           [unitless]

    Returns:
        None 
    """          
    
    # Unpack flight conditions 
    gamma    = freestream.isentropic_expansion_factor
    Cp       = freestream.specific_heat_at_constant_pressure
    
    # Unpack component inputs
    Tt_in    = compressor_conditions.inputs.stagnation_temperature
    Pt_in    = compressor_conditions.inputs.stagnation_pressure 
    PR       = compressor.pressure_ratio
    etapold  = compressor.polytropic_efficiency
    
    # Compute the output properties based on the pressure ratio of the component
    ht_in     = Tt_in*Cp 
    Pt_out    = Pt_in*PR
    Tt_out    = Tt_in*(PR**((gamma-1)/(gamma*etapold)))
    ht_out    = Tt_out*Cp
    
    # Compute the work done by the compressor (normalized by mass flow i.e. J/(kg/s)
    work_done = ht_out - ht_in
    
    # Pack results  
    compressor_conditions.outputs.work_done               = work_done 
    compressor_conditions.outputs.stagnation_temperature  = Tt_out
    compressor_conditions.outputs.stagnation_pressure     = Pt_out
    compressor_conditions.outputs.stagnation_enthalpy     = ht_out
    
    return 

