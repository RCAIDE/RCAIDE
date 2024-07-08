# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Combustor/compute_combustor_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

# ---------------------------------------------------------------------------------------------------------------------- 
# compute_combustor_performance
# ----------------------------------------------------------------------------------------------------------------------    
def compute_combustor_performance(combustor,conditions):
    """ This computes the output values from the input values according to
        equations from the source. The following properties are computed         
        combustor.outputs.
          stagnation_temperature             (numpy.ndarray):  [K]  
          stagnation_pressure                (numpy.ndarray):  [Pa]
          stagnation_enthalpy                (numpy.ndarray):  [J/kg]
          fuel_to_air_ratio                  (numpy.ndarray):  [unitless] 

    Assumptions:
        Constant efficiency and pressure ratio

    Source:
        https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Args:
        conditions.freestream.
          isentropic_expansion_factor        (numpy.ndarray):  [unitless]
          specific_heat_at_constant_pressure (numpy.ndarray):  [J/(kg K)]
          temperature                        (numpy.ndarray):  [K]
          stagnation_temperature             (numpy.ndarray):  [K]
        combustor.inputs.
          stagnation_temperature             (numpy.ndarray):  [K]
          stagnation_pressure                (numpy.ndarray):  [Pa]
          nondim_mass_ratio                  (numpy.ndarray):  [unitless] 
        combustor.
          turbine_inlet_temperature                  (float):  [K]
          pressure_ratio                             (float):  [unitless]
          efficiency                                 (float):  [unitless]
          area_ratio                                 (float):  [unitless]
          fuel_data.specific_energy                  (float):  [J/kg]
      
    Returns:
        None
    """          
    # unpacking the values from conditions 
    Cp      = conditions.freestream.specific_heat_at_constant_pressure 
    
    # unpacking the values form inputs
    Tt_in    = combustor.inputs.stagnation_temperature
    Pt_in    = combustor.inputs.stagnation_pressure
    Tt4      = combustor.turbine_inlet_temperature
    pib      = combustor.pressure_ratio
    eta_b    = combustor.efficiency
    nondim_r = combustor.inputs.nondim_mass_ratio 
    htf      = combustor.fuel_data.specific_energy 
    
    # compute stanation pressure 
    Pt_out  = pib * Pt_in 
    
    #Computing stagnation enthalpies from stagnation temperatures
    ht4     = nondim_r * Cp* Tt4 
    ht_in   = nondim_r * Cp* Tt_in
    
    # Compute the fuel to air ratio using turbine exit temperature, the fuel properties and freestream temperature
    f       = (ht4 - ht_in)/(eta_b*htf-ht4)

    # Computing the exit static and stagnation conditions
    ht_out  = Tt4 * Cp
    
    # Pack results 
    combustor.outputs.stagnation_temperature  = Tt4
    combustor.outputs.stagnation_pressure     = Pt_out
    combustor.outputs.stagnation_enthalpy     = ht_out
    combustor.outputs.fuel_to_air_ratio       = f 
    
    return 
